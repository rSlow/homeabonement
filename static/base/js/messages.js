$(document).ready(function () {
    $('ul.messages > li.message > button.message-closer').on(
        'click',
        function () {
            const message = $(this).parent()
            message.remove()

            const messages = $('ul.messages > li.message')
            if (messages.length === 0) {
                removeList()
            }
        }
    )

    hideMessage()

})

function removeList() {
    $("ul.messages").remove()
}

function hideMessage() {
    setTimeout(function () {
        const messages = $('ul.messages > li.message')
        if (messages.length > 0) {
            const message = messages[0]
            $(message).animate(
                {height: 0, opacity: 0, padding: 0, marginBottom: 0, borderWidth: 0},
                1000,
                function () {
                    $(this).remove()

                    const updatedMessages = $('ul.messages > li.message')
                    if (updatedMessages.length > 0) {
                        hideMessage()
                    } else {
                        removeList()
                    }
                })
        }
    }, 2000)
}

