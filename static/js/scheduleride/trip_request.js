$(document).ready(function(){
    $('#request-ride').click(function(){
        var source = $('#source').val()
        var destination = $('#destination').val()
        var email = $('#email').val()
        var time = $('#time').val()

        if(source && destination && email && time) {
            saveTripRequest(source, destination, time, email)
        }
    })

    setInterval(function(){
        getLogs()
    }, 60 * 1000 * 10)

})

var displayLogs = function(data) {
    var logElement = $('#logging')
    var dataString = data.join("<br />")
    logElement.append('<br/>' + dataString)
}

var getLogs = function() {
    $.ajax({
        type: "GET",
        async: true,
        url: "/api/trip/",
        contentType: "application/json",
        dataType: "json",
        success: function(response) {
            data = response.data
            displayLogs(data)
        },
        error: function(msg) {
            console.log("An error occurred")
        }

    })
}

var saveTripRequest = function(source, destination, time, email) {
    var trip_detail = {
        "source": source,
        "destination": destination,
        "email": email,
        "time_to_reach_dest": time
    }

    $.ajax({
        type: "POST",
        url: "/api/trip/",
        dataType: "json",
        data: JSON.stringify(trip_detail),
        contentType: 'application/json',
        success: function(data) {
            alert("Request saved successfully, we will send you an email to book the cab!")
            console.log("success")
        },
        error: function(err) {
            console.log("An error occurred")
        }
    })

}