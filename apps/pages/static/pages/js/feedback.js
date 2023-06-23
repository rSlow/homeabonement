$(document).ready(function () {
    const files = {}

    $('#feedbackFileInput').on(
        "change", function () {
            const inputFiles = this.files
            for (const file of inputFiles) {
                const fileGUID = generateGuid()
                addFileRow(fileGUID, file)
                files[fileGUID] = file
            }
        }
    )

    $("#feedbackForm").on("submit", function (e) {
        const input = document.querySelector('#feedbackFileInput')
        const filesArray = Array.from(Object.values(files))

        let dt = new DataTransfer();
        filesArray.forEach((file) => {
            dt.items.add(file);
        });
        input.files = dt.files;
        // e.preventDefault()
    })

    function addFileRow(fileGUID, file) {
        const fileBlock = $(".feedback-files")
        fileBlock.append(
            `<div class='feedback-file' id=${fileGUID}>
            <div class="feedback-filename">
                ${file.name}
            </div>
            <button type="button" class="feedback-file-deleter"></button>
        </div>`
        )
        $('.feedback-file-deleter').on('click', function () {
            const fileNode = $(this).parent()
            const fileGUIDAttr = fileNode.attr("id")
            delete files[fileGUIDAttr]
            fileNode.remove()
        })
    }
})


function generateGuid() {
    return Math.random().toString(36).substring(2, 15) +
        Math.random().toString(36).substring(2, 15);
}