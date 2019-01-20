var SWITCHES = [];

var timeoutJobs = {};

function refreshLiveImage() {
    var ts = new Date().getTime();
    $("#liveview").attr("src", "cgi-bin/currentpic.cgi?" + ts);
}
function scheduleRefreshLiveImage(interval) {
    if (timeoutJobs['refreshLiveImage'] != undefined) {
        clearTimeout(timeoutJobs['refreshLiveImage']);
    }
    timeoutJobs['refreshLiveImage'] = setTimeout(refreshLiveImage, interval);
}
function refreshSysUsage() {
    var ts = new Date().getTime();
    $.get("cgi-bin/state.cgi", {cmd: "sysusage", uid: ts}, function(sysusage){document.getElementById("sysusage").innerHTML = sysusage; scheduleRefreshSysUsage(5000);});
}
function scheduleRefreshSysUsage(interval) {
    if (timeoutJobs['refreshSysUsage'] != undefined) {
        clearTimeout(timeoutJobs['refreshSysUsage']);
    }
    timeoutJobs['refreshSysUsage'] = setTimeout(refreshSysUsage, interval);
}
function syncSwitch(sw) {
    var e = $('#' + sw);
    if (!e.prop('disabled')) {
        $.get("cgi-bin/camcontrols.cgi", {
            cmd: "getstate",
            control: sw
        }).done(function (status) {
            // console.log(sw + " status " + status + " / current " + e.prop('checked'));
            e.prop('checked', (status.trim().toLowerCase() == "on"));
        });
    }
}
function syncSwitches() {
    for (var i in SWITCHES) {
        if (timeoutJobs[SWITCHES[i]] != undefined) {
            clearTimeout(timeoutJobs[SWITCHES[i]]);
        }
        syncSwitch(SWITCHES[i]);
    }
}

function showResult(txt) {
    var qv = $("#quickviewDefault");
    var v = $("#quicViewContent");
    if (qv.hasClass("is-active")) {
        // hide first if it's already active
        qv.toggleClass("is-active");
    }
    v.html(txt);
    qv.toggleClass("is-active");
    // auto close after 2.5 seconds
    setTimeout(function () { $("#quickViewClose").click(); }, 2500);
}

$(document).ready(function () {

    setTheme(getThemeChoice());
    
    // Set title page and menu with hostname
    $.get("cgi-bin/state.cgi", {cmd: "hostname"}, function(title){document.title = title;document.getElementById("title").innerHTML = title;});
    
    // Set initial fast camera controls.
    updateCameraControls();
    
    // Load link into #content
    $('.onpage').click(function () {
        var e = $(this);
        var target = e.data('target');
        var cachebuster = "_=" + new Date().getTime();
        if (target.indexOf("?") >= 0) {
            // append as additional param
            cachebuster = "&" + cachebuster;
        } else {
            // new param
            cachebuster = "?" + cachebuster;
        }
        $('#content').load(target + cachebuster);
    });
    // Load link into window
    $('.direct').click(function () {
        window.location.href = $(this).data('target');
    });
    // Ask before proceeding
    $('.prompt').click(function () {
        var e = $(this);
        if (confirm(e.data('message'))) {
            window.location.href = e.data('target');
        }
    });
    // Camera controls
    $(".cam_button").click(function () {
        var b = $(this);
        $.get("cgi-bin/action.cgi?cmd=" + b.data('cmd')).done(function (data) {
            setTimeout(refreshLiveImage, 500);
        });
    });

    // Initial syncing of switches
    timeoutJobs['syncSwitches'] = setTimeout(syncSwitches, 10);
    $('#camcontrol_link').hover(function () {
        // for desktop
        var e = $(this);
        e.toggleClass('is-active');
        if (!e.hasClass('is-active')) {
            return;
        }
        // refresh switches on hover over Camera Controls menu
        if (timeoutJobs['syncSwitches'] != undefined) {
            clearTimeout(timeoutJobs['syncSwitches']);
        }
        timeoutJobs['syncSwitches'] = setTimeout(syncSwitches, 10);
    }, function () { $(this).toggleClass('is-active'); });

    // Hookup navbar burger for mobile
    $('#navbar_burger').click(function () {
        // for mobile
        var e = $(this);
        e.toggleClass('is-active');
        $('#' + e.data('target')).toggleClass('is-active');

        if (!e.hasClass('is-active')) {
            return;
        }
        // refresh switches on burger is tapped
        if (timeoutJobs['syncSwitches'] != undefined) {
            clearTimeout(timeoutJobs['syncSwitches']);
        }
        timeoutJobs['syncSwitches'] = setTimeout(syncSwitches, 10);
    });
    
    // Autohide navbar for mobile
    $('#nav_menu').click(function () {
        // for mobile
        var e = $('#navbar_burger');
        e.toggleClass('is-active');
        $('#' + e.data('target')).toggleClass('is-active');
    });

    // Close action for quickview
    $("#quickViewClose").click(function () {
        $("#quickviewDefault").removeClass("is-active");
    });

    // Use the hash for direct linking
    if (document.location.hash != "") {
        $(document.location.hash).click();
    }

    // Make liveview self refresh
    $("#liveview").attr("onload", "scheduleRefreshLiveImage(1000);");
    
    refreshSysUsage();

});

// set theme cookie
function setCookie(name, value) {
    document.cookie = encodeURIComponent(name) + "=" + encodeURIComponent(value) + "; path=/";
}
// get theme cookie
function getCookie(name) {
    var nameEQ = encodeURIComponent(name) + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ')
            c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0)
            return decodeURIComponent(c.substring(nameEQ.length, c.length));
    }
    return null;
}

function setTheme(c) {
    if (!c) {
        return;
    }
    // clear any existing choice
    $('.theme_choice').removeClass('is-active');

    var theme = $('#theme_choice_' + c);
    theme.addClass('is-active');    // set active
    if (theme.data('css')) {
        // Purge any current custom theme
        $('link.custom_theme').remove();

        // Append css to head
        var css = $('<link>', {
            'class': 'custom_theme',
            'rel': 'stylesheet',
            'href': theme.data('css'),
        });
        $('head').append(css);

        // reapply the custom css
        var customCss = $('#custom_css').clone();
        $('#custom_css').remove()
        $('head').append(customCss);
        setCookie('theme', c);
    }
}

function getThemeChoice() {
    var c = getCookie('theme');
    return c;
}

function cameraControlClick(control)
{   
    var e = $(control);
    e.prop('disabled', true);
    $.get("cgi-bin/camcontrols.cgi", {
        cmd: "getstate",
        control: e.attr('id')
    }).done(function (status) {
        if (status.trim().toLowerCase() == "on") {
            $.get(e.data('unchecked')).done(function (data) {
                e.prop('checked', false);
            });
        } else {
            $.get(e.data('checked')).done(function (data) {
                e.prop('checked', true);
            });
        }
        e.prop('disabled', false);
    });
}


function updateCameraControls() {
    $.get("cgi-bin/camcontrols.cgi?cmd=getcontrols").done(function(data) {
        $("#camcontrol_items").empty();
        SWITCHES = []
        var camControlsArray = eval(data);
        for (var i = 0; i < camControlsArray.length; i++) {
            var camControl = camControlsArray[i];
            SWITCHES.push(camControl.id);
            $("#camcontrol_items").append("<span class=\"navbar-item\"><input id=\"" + camControl.id + "\" \
                onclick='cameraControlClick(this)' \
                type=\"checkbox\" name=\"" + camControl.id + "\" class=\"switch\" \
                data-checked=\"cgi-bin/camcontrols.cgi?cmd=on&control=" + camControl.id + "\" \
                data-unchecked=\"cgi-bin/camcontrols.cgi?cmd=off&control=" + camControl.id + "\"> \
                <label for=\"" + camControl.id + "\">" + camControl.name + "</label></span>");
        }
        
        if (SWITCHES.length > 0) {
          syncSwitches(); 
        }
    });
}
