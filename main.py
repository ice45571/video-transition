# ~/Downloads/ffmpeg-4.0.6/ffmpeg -i video2_25.mp4 -i video4.mp4 -filter_complex " [0:v]split[v0_split0][v0_split1];
# [1:v]split[v1_split0][v1_split1]; [v0_split0]trim=0:11[v0_split0_trim]; [v0_split1]trim=11:12[v0_split1_trim]; [
# v0_split1_trim]setpts=PTS-STARTPTS[v0_split1_trim_pts]; [v1_split0]trim=0:16[v1_split0_trim]; [
# v1_split1]trim=16:17[v1_split1_trim]; [v1_split1_trim]setpts=PTS-STARTPTS[v1_split1_trim_pts]; [
# v0_split1_trim_pts][v1_split0_trim]gltransition=duration=2:source=transitions/circle.glsl",[transitions0]; [
# v0_split0_trim][transitions0][v1_split1_trim_pts]concat=n=3[o]" -map "[o]:0" -c:v libx264 -y out.mp4
import os
import subprocess
import re

ffmpeg = "~/Downloads/ffmpeg-4.0.6/ffmpeg"
ffprobe = "~/Downloads/ffmpeg-4.0.6/ffprobe"
glsls = [
    "transitions/angular.glsl",
    "transitions/Bounce.glsl",
    "transitions/BowTieHorizontal.glsl",
    "transitions/BowTieVertical.glsl",
    "transitions/BowTieWithParameter.glsl",
    "transitions/burn.glsl",
    "transitions/ButterflyWaveScrawler.glsl",
    "transitions/cannabisleaf.glsl",
    "transitions/circle.glsl",
    "transitions/CircleCrop.glsl",
    "transitions/circleopen.glsl",
    "transitions/colorphase.glsl",
    "transitions/ColourDistance.glsl",
    "transitions/CrazyParametricFun.glsl",
    "transitions/crosshatch.glsl",
    "transitions/crosswarp.glsl",
    "transitions/CrossZoom.glsl",
    "transitions/cube.glsl",
    "transitions/Directional.glsl",
    "transitions/directional-easing.glsl",
    "transitions/directionalwarp.glsl",
    "transitions/directionalwipe.glsl",
    "transitions/displacement.glsl",
    "transitions/DoomScreenTransition.glsl",
    "transitions/doorway.glsl",
    "transitions/Dreamy.glsl",
    "transitions/DreamyZoom.glsl",
    "transitions/fade.glsl",
    "transitions/fadecolor.glsl",
    "transitions/fadegrayscale.glsl",
    "transitions/FilmBurn.glsl",
    "transitions/flyeye.glsl",
    "transitions/GlitchDisplace.glsl",
    "transitions/GlitchMemories.glsl",
    "transitions/GridFlip.glsl",
    "transitions/heart.glsl",
    "transitions/hexagonalize.glsl",
    "transitions/InvertedPageCurl.glsl",
    "transitions/kaleidoscope.glsl",
    "transitions/LeftRight.glsl",
    "transitions/LinearBlur.glsl",
    "transitions/luma.glsl",
    "transitions/luminance_melt.glsl",
    "transitions/morph.glsl",
    "transitions/Mosaic.glsl",
    "transitions/multiply_blend.glsl",
    "transitions/perlin.glsl",
    "transitions/pinwheel.glsl",
    "transitions/pixelize.glsl",
    "transitions/polar_function.glsl",
    "transitions/PolkaDotsCurtain.glsl",
    "transitions/Radial.glsl",
    "transitions/randomNoisex.glsl",
    "transitions/randomsquares.glsl",
    "transitions/ripple.glsl",
    "transitions/rotate_scale_fade.glsl",
    "transitions/rotateTransition.glsl",
    "transitions/SimpleZoom.glsl",
    "transitions/squareswire.glsl",
    "transitions/squeeze.glsl",
    "transitions/StereoViewer.glsl",
    "transitions/swap.glsl",
    "transitions/Swirl.glsl",
    "transitions/tangentMotionBlur.glsl",
    "transitions/TopBottom.glsl",
    "transitions/TVStatic.glsl",
    "transitions/undulatingBurnOut.glsl",
    "transitions/WaterDrop.glsl",
    "transitions/wind.glsl",
    "transitions/windowblinds.glsl",
    "transitions/windowslice.glsl",
    "transitions/wipeDown.glsl",
    "transitions/wipeLeft.glsl",
    "transitions/wipeRight.glsl",
    "transitions/wipeUp.glsl",
    "transitions/ZoomInCircles.glsl"
]


def get_file_name(inPath):
    match = re.match("transitions/(.*)\.glsl", inPath)
    return match.group(1)


def get_file_size(inPath):
    size = os.path.getsize(inPath)
    size = size / float(1024 * 1024)
    return round(size, 2)


def get_file_size_format(inPath):
    return str(get_file_size(inPath)) + "mb"


def get_duration(inPath, logFile=None):
    # ffprobe - v
    # error - show_entries
    # format = duration - of
    # default = noprint_wrappers = 1:nokey = 1 - i.\video1.mp4
    code, result = subprocess.getstatusoutput(
        '%s -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i %s' % (ffprobe, inPath))
    if logFile is not None:
        logFile.write("get_duration: path=" + inPath +
                      " size=" + str(get_file_size(inPath)) + "mb" +
                      " code=" + str(code) +
                      " result=" + str(result))
        logFile.write("\n")
    return int(float(result))


def transition_videos(inputList, glslPath, logFile=None):
    def getComplexCmd():
        complexCmd = " -filter_complex \""
        for (index, input) in enumerate(inputList):
            # split、trim
            duration = get_duration(input)
            index = str(index)
            complexCmd = \
                complexCmd + \
                "[" + index + ":v]split[" + index + "split0][" + index + "split1]; " + \
                "[" + index + "split0]trim=0:" + str(duration - 1) + "[" + index + "trim0]; " + \
                "[" + index + "split1]trim=" + str(duration - 1) + ":" + str(duration) + "[" + index + "trim1_tmp]; " + \
                "[" + index + "trim1_tmp]setpts=PTS-STARTPTS[" + index + "trim1]; "
        for (index, input) in enumerate(inputList):
            # transition
            if index > 0:
                complexCmd = \
                    complexCmd + \
                    "[" + str(index - 1) + "trim1][" + str(index) + "trim0]" + \
                    "gltransition=duration=2:source=" + glslPath + "[" + str(index) + "trans]; "

        for (index, input) in enumerate(inputList):
            # concat eg:[v0_split0_trim][transitions0][v1_split1_trim_pts]concat=n=3[o]"
            if index == 0:
                complexCmd = complexCmd + "[" + str(index) + "trim0]"
            else:
                complexCmd = complexCmd + "[" + str(index) + "trans]" + "[" + str(index) + "trim1]"
            if index == (len(inputList) - 1):
                # 最后一个
                complexCmd = complexCmd + "concat=n=" + str(len(inputList) + 1) + "[output]"
        return complexCmd + "\""

    outPutPath = "output/" + get_file_name(glslPath) + ".mp4"
    inputCmd = ""
    complexCmd = getComplexCmd()
    for input in inputList:
        inputCmd = inputCmd + " -i " + input
    cmd = ffmpeg + inputCmd + complexCmd + " -map \"[output]:0\" -c:v libx264 -y " + outPutPath
    print("cmd=" + cmd)
    subprocess.getstatusoutput(cmd)
    print("执行结束 " + outPutPath)

    if logFile is not None:
        msg = ""
        msg += "input:"
        inputSize = 0
        for input in inputList:
            msg += input + "(" + get_file_size_format(input) + ") "
            inputSize += get_file_size(input)
        msg += " output:" + outPutPath + "(" + get_file_size_format(outPutPath) + ") "
        outputSize = get_file_size(outPutPath)
        msg += "存储空间变化量:" + str(round(float(outputSize - inputSize) * 100 / inputSize, 0)) + "%"
        logFile.write(msg)
        logFile.write("\n")
    return


if __name__ == '__main__':
    logFile = open("output/log.txt", "w+")

    for glsl in glsls:
        transition_videos(["input/1.mp4", "input/2.mp4"], glsl, logFile)
    logFile.close()
