$(document).ready(function () {
    const authorOwl = $('#author-carousel');
    authorOwl.owlCarousel({
        dots: false,
        center: true,
        loop: true,
        startPosition: 3,
        items: 3,
        autoplay: true,
        autoplayTimeout: 7e3,
        responsive: {
            690: {
                items: 3,
            },
            400: {
                items: 2,
            },
            0: {
                items: 1,
            },
        }
    });

    $('.slider-button.author-slider-button-prev').click(function () {
        authorOwl.trigger('prev.owl.carousel');
    })

    $('.slider-button.author-slider-button-next').click(function () {
        authorOwl.trigger('next.owl.carousel');
    })
});

$(document).ready(function () {
    const feedbackOwl = $('#feedback-carousel');
    feedbackOwl.owlCarousel({
        dots: false,
        items: 3,
        center: true,
        loop: true,
        margin: 10,
        startPosition: -1,
        // mouseDrag: false,
        responsive: {
            992: {
                items: 3,
            },
            576: {
                items: 2,
            },
            0: {
                items: 1,
            },
        }
    });

    $('#feedback-slider-prev-button').click(function () {
        feedbackOwl.trigger('prev.owl.carousel');
    })

    $('#feedback-slider-next-button').click(function () {
        feedbackOwl.trigger('next.owl.carousel');
    })
});


$(document).ready(function () {
    $('.about-video').css("display", "block")
    const playerSettings = {
        title: "О марафоне",
        controls: [
            'play-large', // The large play button in the center
            'rewind', // Rewind by the seek time (default 10 seconds)
            'play', // Play/pause playback
            'fast-forward', // Fast forward by the seek time (default 10 seconds)
            'progress', // The progress bar and scrubber for playback and buffering
            'current-time', // The current time of playback
            'duration', // The full duration of the media
            'mute', // Toggle mute
            'volume', // Volume control
            'pip', // Picture-in-picture (currently Safari only)
            'fullscreen', // Toggle fullscreen
        ],
        keyboard: {
            focused: true,
            global: true
        },
        seekTime: 5,
    };
    new Plyr('#home-player', playerSettings);
})

$(document).ready(function () {
    new Viewer(
        document.querySelector('#author-carousel'),
        {
            title: false,
            filter(image) {
                const owlWrapper = $(image).parent().parent()
                const isCloned = owlWrapper.hasClass("cloned")
                const isActive = owlWrapper.hasClass("active")
                return isActive || !isCloned;
            },
        }
    );
    new Viewer(
        document.querySelector('#feedback-carousel'),
        {
            title: false,
            filter(image) {
                const owlWrapper = $(image).parent().parent()
                const isCloned = owlWrapper.hasClass("cloned")
                const isActive = owlWrapper.hasClass("active")
                return isActive || !isCloned;
            },
        }
    );
})