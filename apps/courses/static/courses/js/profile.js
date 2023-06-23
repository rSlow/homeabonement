$(".profile-user-block-field").find('input').on(
    "input",
    function () {
        const field = $(this).parent()
        if (!this.value) {
            field.addClass("empty")
        } else {
            field.removeClass("empty")
        }
    })

$('.profile-photo-service > label > input[type=file]').on(
    "change", function () {
        const file = this.files[0]
        if (file.size > 2.5e6) {
            alert("Выбран файл размером более 2.5МБ")
        } else {
            const label = $(this).parent()
            $(label).find("p").html(
                `Выбран файл: ${file.name}`
            )
        }
    }
)

$(".profile-course-tab").hover(
    function () {
        $(this).find(".desc-button").addClass("hover")
    },
    function () {
        $(this).find(".desc-button").removeClass("hover")
    }
)