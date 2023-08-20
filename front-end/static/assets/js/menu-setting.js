"use strict";
document.addEventListener("DOMContentLoaded", function () {
    // =========================================================
    // =========    Menu Customizer [ HTML ] code   ============
    // =========================================================
    // =========================================================
    // ==================    Menu Customizer Start   ===========
    // =========================================================
    // open Menu Styler
    var pctoggle = document.querySelector("#styleSelector > .style-toggler");
    if (pctoggle) {
        pctoggle.addEventListener('click', function () {
            if (!document.querySelector("#styleSelector").classList.contains('open')) {
                document.querySelector("#styleSelector").classList.add("open");
            } else {
                document.querySelector("#styleSelector").classList.remove("open");
            }
        });
    }
    // // layout types
    var layouttypes = document.querySelectorAll(".layout-type > a");
    for (var h = 0; h < layouttypes.length; h++) {
        var c = layouttypes[h];
        c.addEventListener('click', function (event) {
            document.querySelector(".layout-type > a.active").classList.remove("active");
            var targetElement = event.target;
            if (targetElement.tagName == "SPAN") {
                targetElement = targetElement.parentNode;
            }
            targetElement.classList.add("active");
            var temp = targetElement.getAttribute('data-value');
            document.querySelector('head').insertAdjacentHTML("beforeend", '<link rel="stylesheet" class="layout-css" href="">');
            if (temp == "menu-dark") {
                removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'menu-');
                document.querySelector(".pcoded-navbar").classList.add('navbar-dark');
            }
            if (temp == "menu-light") {
                removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'menu-');
                document.querySelector(".pcoded-navbar").classList.remove(('navbar-dark'));
                document.querySelector(".pcoded-navbar").classList.add(temp);
            }
            if (temp == "reset") {
                location.reload();
            }
            if (temp == "dark") {
                removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'menu-');
                document.querySelector(".pcoded-navbar").classList.add("navbar-dark");
                document.querySelector(".layout-css").setAttribute('href', '/static/assets/css/layouts/dark.css');
            } else {
                document.querySelector(".layout-css").setAttribute('href', '');
            }
        });
    }
    // // Header Color
    var headercolor = document.querySelectorAll(".header-color > a");
    for (var h = 0; h < headercolor.length; h++) {
        var c = headercolor[h];
        c.addEventListener('click', function (event) {
            document.querySelector(".header-color > a.active").classList.remove("active");
            var targetElement = event.target;
            if (targetElement.tagName == "SPAN") {
                targetElement = targetElement.parentNode;
            }
            targetElement.classList.add("active");
            var temp = targetElement.getAttribute('data-value');
            if (temp == "header-default") {
                removeClassByPrefix(document.querySelector(".pcoded-header"), 'header-');
            } else {
                removeClassByPrefix(document.querySelector(".pcoded-header"), 'header-');
                document.querySelector(".pcoded-header").classList.add(temp);
            }
        });
    }
    // // Menu Color
    var menucolor = document.querySelectorAll(".navbar-color > a");
    for (var h = 0; h < menucolor.length; h++) {
        var c = menucolor[h];
        c.addEventListener('click', function (event) {
            document.querySelector(".navbar-color > a.active").classList.remove("active");
            var targetElement = event.target;
            if (targetElement.tagName == "SPAN") {
                targetElement = targetElement.parentNode;
            }
            targetElement.classList.add("active");
            var temp = targetElement.getAttribute('data-value');
            if (temp == "navbar-default") {
                removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'navbar-');
            } else {
                removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'navbar-');
                document.querySelector(".pcoded-navbar").classList.add(temp);
            }
        });
    }
    // // Active Color
    var activecolor = document.querySelectorAll(".active-color > a");
    for (var h = 0; h < activecolor.length; h++) {
        var c = activecolor[h];
        c.addEventListener('click', function (event) {
            document.querySelector(".active-color > a.active").classList.remove("active");
            var targetElement = event.target;
            if (targetElement.tagName == "SPAN") {
                targetElement = targetElement.parentNode;
            }
            targetElement.classList.add("active");
            var temp = targetElement.getAttribute('data-value');
            if (temp == "active-default") {
                removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'active-');
            } else {
                removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'active-');
                document.querySelector(".pcoded-navbar").classList.add(temp);
            }
        });
    }
    // // rtl layouts
    var rtllayout = document.querySelector("#theme-rtl");
    rtllayout.addEventListener('click', function () {
        document.querySelector('head').insertAdjacentHTML("beforeend", '<link rel="stylesheet" class="rtl-css" href="">');
        if (rtllayout.checked) {
            document.querySelector(".rtl-css").setAttribute('href', '../assets/css/layouts/rtl.css');
        } else {
            document.querySelector(".rtl-css").setAttribute('href', '');
        }
    });
    // // Menu Fixed
    var Menufixed = document.querySelector("#menu-fixed");
    Menufixed.addEventListener('click', function () {
        if (Menufixed.checked) {
            document.querySelector(".pcoded-navbar").classList.remove("menupos-static");
        } else {
            document.querySelector(".pcoded-navbar").classList.add("menupos-static");
            setTimeout(function () {
                document.querySelector('.navbar-content').style.cssText = `
                    overflow: visible;
                    height: calc(100% - 70px);
                `;
            }, 400);
        }
    });
    // // Header Fixed
    var Headerfixed = document.querySelector("#header-fixed");
    Headerfixed.addEventListener('click', function () {
        if (Headerfixed.checked) {
            document.querySelector(".pcoded-header").classList.add("headerpos-fixed");
            document.querySelector(".pcoded-header").classList.add("header-blue");
            document.querySelector(".header-color > a.active").classList.remove("active");
            document.querySelector(".header-color > a[data-value='header-blue']").classList.add("active");
        } else {
            document.querySelector(".pcoded-header").classList.remove("headerpos-fixed");
        }
    });
    // // Menu Icon Color
    var Menuicon = document.querySelector("#icon-colored");
    Menuicon.addEventListener('click', function () {
        if (Menuicon.checked) {
            document.querySelector(".pcoded-navbar").classList.add("icon-colored");
        } else {
            document.querySelector(".pcoded-navbar").classList.remove("icon-colored");
        }
    });
    // // Box layouts
    var boxlayout = document.querySelector("#box-layouts");
    boxlayout.addEventListener('click', function () {
        if (boxlayout.checked) {
            document.querySelector("body").classList.add("container");
            document.querySelector("body").classList.add("box-layout");
        } else {
            document.querySelector("body").classList.remove("container");
            document.querySelector("body").classList.remove("box-layout");
        }
    });
    // // Caption Hide
    var captionhide = document.querySelector("#caption-hide");
    captionhide.addEventListener('click', function () {
        if (captionhide.checked) {
            document.querySelector(".pcoded-navbar").classList.add("caption-hide");
        } else {
            document.querySelector(".pcoded-navbar").classList.remove("caption-hide");
        }
    });

    // // Menu image background
    var Menuimage = document.querySelectorAll(".navbar-images > a");
    for (var h = 0; h < Menuimage.length; h++) {
        var c = Menuimage[h];
        c.addEventListener('click', function (event) {
            if (!!document.querySelector('.navbar-images > a.active')) {
                document.querySelector(".navbar-images > a.active").classList.remove("active");
            }
            var targetElement = event.target;
            if (targetElement.tagName == "SPAN") {
                targetElement = targetElement.parentNode;
            }
            targetElement.classList.add("active");
            var temp = targetElement.getAttribute('data-value');
            removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'menu-');
            removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'navbar-image-');
            document.querySelector(".pcoded-navbar").classList.add(temp);
        });
    }
    // // title Color
    var activecolor = document.querySelectorAll(".title-color > a");
    for (var h = 0; h < activecolor.length; h++) {
        var c = activecolor[h];
        c.addEventListener('click', function (event) {
            document.querySelector(".title-color > a.active").classList.remove("active");
            var targetElement = event.target;
            if (targetElement.tagName == "SPAN") {
                targetElement = targetElement.parentNode;
            }
            targetElement.classList.add("active");
            var temp = targetElement.getAttribute('data-value');
            if (temp == "title-default") {
                removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'title-');
            } else {
                removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'title-');
                document.querySelector(".pcoded-navbar").classList.add(temp);
            }
        });
    }
    // // brand Color
    var brandcolor = document.querySelectorAll(".brand-color > a");
    for (var h = 0; h < brandcolor.length; h++) {
        var c = brandcolor[h];
        c.addEventListener('click', function (event) {
            document.querySelector(".brand-color > a.active").classList.remove("active");
            var targetElement = event.target;
            if (targetElement.tagName == "SPAN") {
                targetElement = targetElement.parentNode;
            }
            targetElement.classList.add("active");
            var temp = targetElement.getAttribute('data-value');
            if (temp == "brand-default") {
                removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'brand-');
            } else {
                removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'brand-');
                document.querySelector(".pcoded-navbar").classList.add(temp);
            }
        });
    }
    // ==================    Menu Customizer End   =============
    // =========================================================
});
// Menu Dropdown icon
function drpicon(temp) {
}
// Menu subitem icon
function menuitemicon(temp) {
}

function removeClassByPrefix(node, prefix) {
    for (let i = 0; i < node.classList.length; i++) {
        let value = node.classList[i];
        if (value.startsWith(prefix)) {
            node.classList.remove(value);
        }
    }
}
 //We handle our user interaction here.
 themeSwitch.addEventListener('change', function() {
    
    if (this.checked) {
        changeMode(0)
    } else {
        changeMode(1)
    }
});
