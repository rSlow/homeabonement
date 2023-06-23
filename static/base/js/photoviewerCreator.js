// function createPhotoViewer(selector, filterSelector = null) {
//     $(selector).on('mousedown', function () {
//         const startTime = Date.now()
//
//         $(this).on('mouseup', function () {
//             const endTime = Date.now()
//             if (endTime - startTime < 100) {
//                 let items = []
//
//                 let updatedSelector;
//                 if (filterSelector) {
//                     const selectorArray = selector.split(" ")
//                     selectorArray.splice(
//                         selectorArray.length - 1,
//                         0,
//                         filterSelector
//                     )
//                     updatedSelector = selectorArray.join(" ")
//                 } else {
//                     updatedSelector = selector
//                 }
//
//                 $(updatedSelector).each(function () {
//                     const src = $(this).attr('src');
//                     items.push({
//                         src: src
//                     });
//                 });
//                 const itemSrc = $(this).attr('src')
//                 const originalItem = $(updatedSelector + `[src='${itemSrc}']`)
//
//                 const options = {
//                     index: $(updatedSelector).index(originalItem),
//                     draggable: false,
//                     title: false,
//                     initMaximized: true,
//                     resizable: false,
//                     headerToolbar: ['close'],
//                     keyboard: false,
//                     i18n: {
//                         close: 'Закрыть',
//                         zoomIn: 'Увеличить (+)',
//                         zoomOut: 'Уменьшить (-)',
//                         prev: 'предыдущее (←)',
//                         next: 'следующее (→)',
//                         fullscreen: 'На полный экран',
//                         actualSize: 'Расширить',
//                         rotateLeft: 'Повернуть против часовой',
//                         rotateRight: 'Повернуть против часовой',
//                     }
//                 };
//                 const viewer = new PhotoViewer(items, options);
//
//                 $(".photoviewer-stage").on('click', function () {
//                     viewer.close()
//                 })
//                 $('.photoviewer-image').on('click', function (e) {
//                     e.stopPropagation()
//                 })
//             }
//         })
//     })
// }

class CustomPhotoViewer {
    options = {
        draggable: false,
        title: false,
        initMaximized: true,
        resizable: false,
        headerToolbar: ['close'],
        keyboard: false,
        i18n: {
            close: 'Закрыть',
            zoomIn: 'Увеличить (+)',
            zoomOut: 'Уменьшить (-)',
            prev: 'предыдущее (←)',
            next: 'следующее (→)',
            fullscreen: 'На полный экран',
            actualSize: 'Расширить',
            rotateLeft: 'Повернуть против часовой',
            rotateRight: 'Повернуть против часовой',
        }
    };
    photoViewerStage=".photoviewer-stage"
    photoViewerImage=".photoviewer-image"

    constructor(selector,
                filterSelector = null,
                timeDelay = 100,
                attr = "src",
                closeOnWrapperClick = true,
    ) {
        this.selector = selector
        this.filterSelector = filterSelector
        this.timeDelay = timeDelay
        this.attr = attr
        this.closeOnWrapperClick = closeOnWrapperClick

        this.initialize()
    }

    getSelector() {
        let selector;
        if (this.filterSelector) {
            const selectorArray = this.selector.split(" ")
            selectorArray.splice(
                selectorArray.length - 1,
                0,
                this.filterSelector
            )
            selector = selectorArray.join(" ")
        } else {
            selector = this.selector
        }
        return selector
    }

    getItems() {
        const selector = this.getSelector()
        const items = []
        const thisAttr = this.attr
        $(selector).each(function () {
            const attr = $(this).attr(thisAttr);
            items.push({
                src: attr
            });
        });
        return items;
    }

    getOriginalIndex(clickedItem) {
        const updatedSelector = this.getSelector()
        const itemAttr = $(clickedItem).attr(this.attr)
        const originalItem = $(updatedSelector + `[${this.attr}='${itemAttr}']`)
        return $(updatedSelector).index(originalItem)
    }

    initialize() {
        $(this.selector).on('mousedown', () => {
            const startTime = Date.now()

            $(this.selector).on('mouseup', (e) => {
                const clickedItem = e.target
                const endTime = Date.now()

                if (endTime - startTime < this.timeDelay) {
                    const items = this.getItems()
                    const originalIndex = this.getOriginalIndex(clickedItem)

                    const optionsWithIndex = {...this.options, index: originalIndex}
                    this.viewer = new PhotoViewer(items, optionsWithIndex);
                    if (this.closeOnWrapperClick) {
                        this.initOnClose()
                    }
                }
            })
        })
    }

    initOnClose() {
        if (this.viewer) {
            $(this.photoViewerStage).on('click', () => {
                this.viewer.close()
            })
            $(this.photoViewerImage).on('click', (e) => {
                e.stopPropagation()
            })
        }
    }
}