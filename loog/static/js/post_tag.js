const assignmentEndpoint = "/api/discovery/v1/user-assignments/";
const tagEndpoint = "/api/discovery/v1/tags/";

function submit_tags() {
    let length = $(".tag-text-input").length;
    $(".tag-text-input").each(function(index) {
        let receiverID = $(this).attr("data-userid");
        document.getElementById("btn_submit").disabled = true;
        $(this).val().split(",").forEach(function(element, idx, arr) {
            $.ajax({
                url: tagEndpoint,
                method: 'POST',
                data: { "name": element },
                success: function(data) {
                    $.ajax({
                        url: assignmentEndpoint,
                        method: 'POST',
                        data: {
                            "tag": data.id,
                            "giver": UserID,
                            "receiver": receiverID
                        },
                        success: function(data) {
                            console.log(data);
                            if (index === length - 1 && idx === arr.length - 1) {
                                window.location.href = "/";
                            }
                        },
                        error: function(error) {
                            console.error(error);
                        }
                    });
                },
                error: function(error) {
                    console.error(error);
                }
            });
        });
    });
    return false;
}