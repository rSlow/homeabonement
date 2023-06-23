$(document).ready(function () {
    const links = $(".js-inline-admin-formset .form-row.has_original p[class$=-upload] a")
    for (const link of links) {
        const linkElem = $(link)
        linkElem.attr("target", "_blank")
        $(`<a download href="${linkElem.attr('href')}"> Скачать файл </a>`).insertAfter(linkElem)
        $('<span> | </span>').insertAfter(linkElem)
    }
})