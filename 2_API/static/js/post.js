$(function () {
  var file = null;
  var blob = null;

  $("input[type=file]").change(function () {
    file = $(this).prop("files")[0];

    //File check
    if (file.type != "image/jpeg" && file.type != "image/png") {
      file = null;
      blob = null;
      return;
    }

    var result = document.getElementById("result");
    result.innerHTML = "";

    //Resize the image
    var image = new Image();
    var reader = new FileReader();
    reader.onload = function (e) {
      image.onload = function () {
        var width, height;
        width = image.width
        height = image.height
        var canvas = $("#canvas").attr("width", width).attr("height", height);
        var ctx = canvas[0].getContext("2d");
        ctx.clearRect(0, 0, width, height);
        ctx.drawImage(
          image,
          0,
          0,
          image.width,
          image.height,
          0,
          0,
          width,
          height
        );

        //Get base64 image data from canvas and create Blob for POST
        var base64 = canvas.get(0).toDataURL("image/jpeg");
        var barr, bin, i, len;
        bin = atob(base64.split("base64,")[1]);
        len = bin.length;
        barr = new Uint8Array(len);
        i = 0;
        while (i < len) {
          barr[i] = bin.charCodeAt(i);
          i++;
        }
        blob = new Blob([barr], { type: "image/jpeg" });
        console.log(blob);
      };
      image.src = e.target.result;
    };
    reader.readAsDataURL(file);
  });

  //When the upload start button is clicked
  $("#post").click(function () {
    if (!file || !blob) {
      return;
    }

    var name,
      fd = new FormData();
    fd.append("files", blob, file.name);

    //POST to API
    $.ajax({
      url: "/process",
      type: "POST",
      dataType: "json",
      data: fd,
      processData: false,
      contentType: false,
    })
      .done(function (data, textStatus, jqXHR) {
          //If communication is successful, output the result
        var response = JSON.stringify(data);
        var response = JSON.parse(response);
        console.log(response);
        var result = document.getElementById("result");
        result.innerHTML = response[file.name];
      })
      .fail(function (jqXHR, textStatus, errorThrown) {
          //If communication fails, an error message will be output.
        var result = document.getElementById("result");
        result.innerHTML = "Communication with the server failed...";
      });

    $.ajax({
      url: "/save_img",
      type: "POST",
      dataType: "json",
      data: fd,
      processData: false,
      contentType: false,
    })
      .done(function (data, textStatus, jqXHR) {
          //If communication is successful, output the result
        var response = JSON.stringify(data);
        var response = JSON.parse(response);
        console.log(response);
      })
      .fail(function (jqXHR, textStatus, errorThrown) {
          //If communication fails, an error message will be output.
        console.log(response)
      });

  });
});
