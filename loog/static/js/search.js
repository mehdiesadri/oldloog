const entryPoint = "/api/discovery/v1/search-user/";
let allowed = true;

function reset() {
    $("#txt_query").val("");
    $("#loading").toggleClass("d-none");
    allowed = true;
}

function search() {
    let query = $("#txt_query").val();
    if (query && allowed) {
        $("#loading").toggleClass("d-none");
        $.ajax({
            url: entryPoint,
            method: 'GET',
            data: { 'query': query },
            success: function(data) {
                if (data.count === 0) {
                    alert("No user found!");
                    reset();
                } else {
                    setTimeout(function() {
                        alert("No user found!");
                        reset();
                    }, 30000);
                    allowed = false;
                }
            },
            error: function(error) {
                if (error.status === 403) {
                    alert("Please login first!");
                } else {
                    alert("Please check the internet connection!")
                }
                reset();
                console.error(error);
            }
        });
    }

    return false;
}