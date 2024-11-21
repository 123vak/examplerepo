
$(document).ready(function() {

// Function to get a cookie value by name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

console.log(branchviewurl)
$('#btnsearch').on('click',function(){
    console.log("hello")
    $.ajax({
        url : branchviewurl,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            branchname: $("#branchName").val(),
            branchcode: $("#branchCode").val()
        }),
        headers: {
            'X-CSRFToken': csrftoken 
        },
        success:function(response){
            console.log(response)
            var html = '';

            var data = response.data;
            html += '<thead><tr>';
            if (data.length > 0 && data[0].length > 0) {
                var firstObject = data[0][0]; 
                for (var key in firstObject) {
                    if (firstObject.hasOwnProperty(key)) {
                        html += '<th>' + key + '</th>';
                    }
                }
                html += '</tr></thead>';
            }
            
            html += '<tbody>';
            for (var i = 0; i < data.length; i++) {
                for (var j = 0; j < data[i].length; j++) {
                    var obj = data[i][j];
                    html += '<tr>';
                    for (var key in obj) {
                        if (obj.hasOwnProperty(key)) {
                            html += '<td>' + obj[key] + '</td>';
                        }
                    }
                    html += '</tr>';
                }
            }
            html += '</tbody>';
            
            $('#tableid').html(html);
            
        },
        error:function(e){

        }

    })

})



$("#bnupload").on('click',function(){
    var formData = new FormData();  
    formData.append('excel_file', $('#excelFileInput')[0].files[0]);

    $.ajax({
        url:fileuploadurl,
        data:formData,
        type:"POST",
        contentType: false,  
        processData: false, 
        headers: {
            'X-CSRFToken': csrftoken 
        },
        success: function(response) {
            console.log('File uploaded successfully:', response);
        },
        error: function(xhr, status, error) {
            console.error('Upload failed:', error);
        }
        
    })

})
})


