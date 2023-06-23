$(document).ready(function () {
    $("a[href^='#']").on("click", function () {
        let href = $(this).attr("href");

        $("html, body").animate({
                scrollTop: $(href).offset().top - 100
            },
            750);

        return false;
    });

    function setHTMLVh() {
        function resizeWindow() {
            let vh = window.innerHeight * 0.01;
            document.documentElement.style.setProperty('--vh', `${vh}px`);
        }

        window.addEventListener('resize', resizeWindow);
        resizeWindow()
    }

    setHTMLVh()

    const referrer = document.referrer
    if (referrer) {
        const btn = $("a.back-button")
        btn.attr("href", referrer)
        btn.css({"display": "block"})
    }
})


