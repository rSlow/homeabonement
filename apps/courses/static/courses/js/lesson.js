$(document).ready(function () {
    $('.lesson-video').css("display", "block")
    // resizeCallback()
    // $(window).resize(resizeCallback)
    const player = new Plyr('#player');
})

const aspect = 16 / 9

function resizeCallback() {
    const videoDiv = $('.lesson-video')
    const videoDivWidth = videoDiv.width()

    const video = $(videoDiv).find('video')
    video.css("display", "block")
    video.css("width", videoDivWidth)
    video.css("height", videoDivWidth / aspect)

}