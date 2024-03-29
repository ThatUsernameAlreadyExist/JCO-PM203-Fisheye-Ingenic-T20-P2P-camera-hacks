$(document).ready(function() {
  $('#formResolution').submit(function(event) {
    var b = $('#resSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'videouser': $('input[name=videouser]').val(),
      'videopassword': $('input[name=videopassword]').val(),
      'videoport': $('input[name=videoport]').val(),
      'video_size': $('select[name=video_size]').val(),
      'video_format': $('select[name=video_format]').val(),
      'brbitrate' : $('input[name=brbitrate]').val(),
      'frmRateDen': $('input[name=frmRateDen]').val(),
      'frmRateNum': $('input[name=frmRateNum]').val(),
    };
    $.ajax({
      type: 'POST',
      url: $('#formResolution').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      showResult(res);
      // reload after 2s
      setTimeout(function() {
        $('#content').load('cgi-bin/status.cgi');
      }, 2000);
    });
    event.preventDefault();
  });

  $('#tzForm').submit(function(event) {
    var b = $('#tzSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'tz': $('input[name=tz]').val(),
      'hostname': $('input[name=hostname]').val(),
      'ntp_srv': $('input[name=ntp_srv]').val()
    };
    $.ajax({
      type: 'POST',
      url: $('#tzForm').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      showResult(res);
      // reload after 2s
      setTimeout(function() {
        $('#content').load('cgi-bin/status.cgi');
      }, 2000);
    });
    event.preventDefault();
  });

  $('#passwordForm').submit(function(event) {
    var b = $('#pwSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'password': $('input[name=httppassword]').val(),
    };
    $.ajax({
      type: 'POST',
      url: $('#passwordForm').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      showResult(res);
      // reload after 2s
      setTimeout(function() {
        $('#content').load('cgi-bin/status.cgi');
      }, 2000);
    });
    event.preventDefault();
  });

  $('#allPasswordForm').submit(function(event) {
    var b = $('#allpwSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'password': $('input[name=allpassword]').val(),
    };
    $.ajax({
      type: 'POST',
      url: $('#allPasswordForm').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      showResult(res);
      // reload after 2s
      setTimeout(function() {
        $('#content').load('cgi-bin/status.cgi');
      }, 2000);
    });
    event.preventDefault();
  });

  $('#telnetForm').submit(function(event) {
    var b = $('#telnetSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'telnetport': $('input[name=telnetport]').val(),
    };
    $.ajax({
      type: 'POST',
      url: $('#telnetForm').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      showResult(res);
      // reload after 2s
      setTimeout(function() {
        $('#content').load('cgi-bin/status.cgi');
      }, 2000);
    });
    event.preventDefault();
  });

  $('#ftpForm').submit(function(event) {
    var b = $('#ftpSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'ftpport': $('input[name=ftpport]').val(),
      'ftpuser': $('input[name=ftpuser]').val(),
      'ftppassword': $('input[name=ftppassword]').val(),
    };
    $.ajax({
      type: 'POST',
      url: $('#ftpForm').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      showResult(res);
      // reload after 2s
      setTimeout(function() {
        $('#content').load('cgi-bin/status.cgi');
      }, 2000);
    });
    event.preventDefault();
  });

  $('#formOSD').submit(function(event) {
    var b = $('#osdSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    if ($('input[name=OSDenable]').prop('checked')) {
      osdenable = 'enabled';
    } else {
      osdenable = '';
    }
    if ($('input[name=AXISenable]').prop('checked')) {
      axisenable = 'enabled';
    } else {
      axisenable = '';
    }
    var formData = {
      'OSDenable': osdenable,
      'AXISenable': axisenable,
      'osdtext': $('input[name=osdtext]').val(),
      'color': $('select[name=color]').val(),
      'OSDSize': $('input[name=OSDSize]').val(),
      'fontName': $('select[name=FontName]').val(),
      'spacepixels': $('input[name=spacepixels]').val(),
      'posy': $('input[name=posy]').val(),
      'fixedw': $('select[name=fixedw]').val()
    };
    $.ajax({
      type: 'POST',
      url: $('#formOSD').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));
      showResult(res);
    });
    event.preventDefault();
  });

  $('#formRecording').submit(function(event) {
    var b = $('#recSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    if ($('input[name=motion_act]').prop('checked')) {
          motion_act = '1';
      } else {
          motion_act = '0';
      }
    var formData = {
      'motion_act': motion_act,
      'postrec': $('input[name=postrec]').val(),
      'maxduration': $('input[name=maxduration]').val(),
      'diskspace': $('input[name=diskspace]').val()
    };
    $.ajax({
      type: 'POST',
      url: $('#formRecording').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));
      showResult(res);
    });
    event.preventDefault();
  });

  $('#formTimelapse').submit(function(event) {
    var b = $('#tlSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'tlinterval': $('input[name=tlinterval]').val(),
      'tlduration': $('input[name=tlduration]').val()
    };
    $.ajax({
      type: 'POST',
      url: $('#formTimelapse').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));
      showResult(res);
    });
    event.preventDefault();
  });

  $('#formaudioin').submit(function(event) {
      var b = $('#audioinSubmit');

      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));
      if ($('input[name=HFEnabled]').prop('checked')) {
          HFEnabled = 'true';
      } else {
          HFEnabled = 'false';
      }
      if ($('input[name=AECEnabled]').prop('checked')) {
        AECEnabled = 'true';
      } else {
        AECEnabled = 'false';
      }

      var formData = {
        'audioinFormat': $('select[name=audioinFormat]').val(),
        'audioinBR': $('select[name=audioinBR]').val(),
        'audiooutBR': $('select[name=audiooutBR]').val(),
        'audioinFilter': $('select[name=audioinFilter]').val(),
        'HFEnabled': HFEnabled,
        'AECEnabled': AECEnabled,
        'audioinVol': $('input[name=audioinVol]').val()

      };
      $.ajax({
        type: 'POST',
        url: $('#formaudioin').attr('action'),
        data: formData,
        dataType: 'html',
        encode: true
      }).done(function(res) {

        b.toggleClass('is-loading');
        b.prop('disabled', !b.prop('disabled'));
        showResult(res);
      });
      event.preventDefault();
    });

  $('#formAudio').submit(function(event) {
      var b = $('#AudioTestSubmit');

      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      var formData = {
        'audioSource': $('select[name=audioSource]').val(),
        'audiotestVol': $('input[name=audiotestVol]').val(),

      };
      $.ajax({
        type: 'POST',
        url: $('#formAudio').attr('action'),
        data: formData,
        dataType: 'html',
        encode: true
      }).done(function(res) {

        b.toggleClass('is-loading');
        b.prop('disabled', !b.prop('disabled'));
        showResult(res);
      });
      event.preventDefault();
    });

    $('#flip').change(function() {
        if($(this).is(":checked")) {
           // if checked
           $.ajax({
            'url': 'cgi-bin/action.cgi?cmd=flip-on',
           })
        }  else {
            $.ajax({
                'url': 'cgi-bin/action.cgi?cmd=flip-off',
            })
        }
    });
    
    $('#enable_rtsp_log').change(function() {
        if($(this).is(":checked")) {
           // if checked
           $.ajax({
            'url': 'cgi-bin/action.cgi?cmd=rtsp-log-on',
           })
        }  else {
            $.ajax({
                'url': 'cgi-bin/action.cgi?cmd=rtsp-log-off',
            })
        }
    });
    
    $('#formPtt').submit(function(event) {
      var b = $('#pttSubmit');

      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      var formData = {
        'audiooutVol': $('input[name=audiooutVol]').val(),
      };
      $.ajax({
        type: 'POST',
        url: $('#formPtt').attr('action'),
        data: formData,
        dataType: 'html',
        encode: true
      }).done(function(res) {

        b.toggleClass('is-loading');
        b.prop('disabled', !b.prop('disabled'));
        showResult(res);
      });
      event.preventDefault();
    });
});
