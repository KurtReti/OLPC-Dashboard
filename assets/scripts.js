// click export as csv button to initiate download
jQuery(document).on("click", "a[data-title='Export Chart Data']", function(e){
    jQuery(e.currentTarget).parents("div.dash-graph").siblings("button[role='export']").click()
})

// convert timestamp to a date string
function to_date(timestamp){
    return new Date(Number.parseInt(timestamp) * 1000).toLocaleDateString("en-AU")
}

// wait for an element to be available in the DOM and then process callback
function waitForElement(selector, callback) {
        if (document.querySelector(selector)) {
            callback(document.querySelector(selector));
        }

        const observer = new MutationObserver(mutations => {
            if (document.querySelector(selector)) {
               callback(document.querySelector(selector));
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true,
        });
}

// wait for an element to change text and then process callback
function waitForTextChange(target, callback) {
        const observer = new MutationObserver(mutations => {
            callback()
        });

        observer.observe(target, {
            characterData: true, childList: true, oldCharacterData: true, subtree: true
        });
}

// since dash doesn't natively have ability to format timestamp in slider add workaround
function dateTooltips(){
    // once tooltip is available add as date and wait for text change
    waitForElement(".tooltip-as-date .rc-slider-tooltip-inner:not(.as-date)", function (elm){
        var elemDiv = document.createElement('div');
        elemDiv.className="rc-slider-tooltip-inner-date"
        elm.parentNode.appendChild(elemDiv);
        elm.className += " as-date"
        elemDiv.textContent = to_date(elm.textContent)
        waitForTextChange(elm, function(){
            elemDiv.textContent = to_date(elm.textContent)
        })
    })
}

dateTooltips()

function canvasImage () {
    var canvas = document.createElement("canvas");
    var context = canvas.getContext("2d");
    var elements = document.getElementsByClassName("email");
    for(element of elements){
        canvas.width = parseInt(text_dimensions.width)
        canvas.height = 20
        context.font = "16px Arial";
        text_dimensions = context.measureText(element.getAttribute("data-title"))
        context.fillText(element.getAttribute("data-title"), 0, 8);
        element.src=canvas.toDataURL('image/png')
        console.log(canvas)
    }
 }