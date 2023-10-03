

// Input date string

function date_get() {
    const dateString = "2023-09-12T07:14:33.822Z";

    // Create a Date object from the input string
    const date = new Date(dateString);

    // Define an array of month names
    const monthNames = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ];

    // Get the day, month, and year components from the Date object
    const day = date.getDate();
    const month = monthNames[date.getMonth()];
    const year = date.getFullYear();

    // Format the date in the desired format
    const formattedDate = `${day} ${month}, ${year}`;

    console.log(formattedDate); // Output: "12 Sep, 2023"


}
date_get();

function loading() {
    $('#table1').html('<tr><td colspan="6"><div class="d-flex justify-content-center"> <div class="spinner-border" role="status"> <span class="sr-only"></span> </div> </div></td></tr>');

}


console.log("Ajax Loaded");
//Task adding ajax
$('#task_add').click(function () {
    $("#modal_form")[0].reset();
});

$('#task_save').click(function () {
    console.log("Save");
    let id_task_name = $("#id_task_name").val();
    let id_deadline = $("#id_deadline").val();
    console.log(id_task_name);
    console.log(id_deadline);


    let csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();

    if (id_task_name == "") {
        console.log("please enter name");
    } else if (id_deadline == "") {
        console.log("please select deadline");

        //make data validation
        const date = new Date();
        console.log(date.getFullYear() + '-' + date.getMonth() + '-' + date.getDate());

    } else {
        loading();

        mydata = { 'id_task_name': id_task_name, 'id_deadline': id_deadline, 'csrfmiddlewaretoken': csrfmiddlewaretoken };
        $.ajax({
            url: "/task-save/",
            method: "POST",
            data: mydata,
            success: function (data) {
                if (data.status == 'Save') {
                    output = '';
                    //hide modal
                    $('#exampleModal').modal('hide');
                    task = data.user_task_list;
                    output = show_table(task, output);
                    setTimeout(function () {
                        $("#table1").html(output);
                    }, 1000);
                    $('#modal_form')[0].reset;

                }
            },
        });
    }
})


$("tbody").on("click", ".btn-del", function () {
    let id_task_id = $(this).attr("data-sid");
    //csrf
    let csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
    loading();


    mydata = { 'id_task_id': id_task_id, 'csrfmiddlewaretoken': csrfmiddlewaretoken };
    $.ajax({
        url: "/task-delete/",
        method: "POST",
        data: mydata,
        success: function (data) {
            //console.log(data);
            if (data.status == 'Save') {
                output = '';
                //hide modal
                $('#exampleModal').modal('hide');
                task = data.user_task_list;
                output = show_table(task, output);
                setTimeout(function () {
                    $("#table1").html(output);
                }, 1000);

            }
        },
    });




});

//mark complete
$("tbody").on("click", ".btn-complete", function () {
    let id_task_id = $(this).attr("data-sid");

    //csrf
    let csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
    loading();


    mydata = { 'id_task_id': id_task_id, 'csrfmiddlewaretoken': csrfmiddlewaretoken };
    $.ajax({
        url: "/task-complete/",
        method: "POST",
        data: mydata,
        success: function (data) {
            if (data.status == 'Save') {
                output = '';
                task = data.user_task_list;
                output = show_table(task, output);
                setTimeout(function () {
                    $("#table1").html(output);
                }, 500);

            }
        },
    });




});



//mark incomplete
$("tbody").on("click", ".btn-incomplete", function () {
    let id_task_id = $(this).attr("data-sid");
    //csrf
    let csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
    loading();

    mydata = { 'id_task_id': id_task_id, 'csrfmiddlewaretoken': csrfmiddlewaretoken };
    $.ajax({
        url: "/task-incomplete/",
        method: "POST",
        data: mydata,
        success: function (data) {
            if (data.status == 'Save') {
                output = '';
                task = data.user_task_list;
                output = show_table(task, output);
                setTimeout(function () {
                    $("#table1").html(output);
                }, 1000);

            }
        },
    });




});


//Table forming

function show_table(task, output) {
    $('#exampleModal').modal('hide');

    if (task.length > 0) {
        $("#task_list").show();
        $("#no_task_list").hide();
    } else {
        $("#task_list").hide();
        $("#no_task_list").show();
    }
    let count = 0;
    for (i = 0; i < task.length; i++) {
        count = i + 1;
        output += '<tr><th scope="row">' + count + '</th><td>' + task[i].task_name + '</td><td>' + task[i].deadline + '</td> <td>' + task[i].added_on.slice(0, 10) + '</td> <td>';

        if (task[i].is_completed) {
            output += '<span class="badge badge-success">Completed</span></td><td><input type="submit" class="btn btn-warning btn-sm btn-incomplete" data-sid="' + task[i].id + '" value="Mark Incomplete">';
        } else { output += '<span class="badge badge-warning">Incomplete</span></td><td><input type="submit" class="btn btn-success btn-sm btn-complete" data-sid="' + task[i].id + '" value="Mark Complete">'; }
        output += '<input type="submit" class="btn btn-danger btn-sm btn-del" data-sid="' + task[i].id + '" value="Delete"</td></tr>';

    }

    return output;
}

function ajaxcall() {
    let csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
    console.log('CALLING')

    
    $.post("/task-sort/", 
    {
            sort_by: $('input:radio[name="btnradiob"]:checked').val(),
            order: $('input:radio[name="btnradioa"]:checked').val(),
            csrfmiddlewaretoken: csrfmiddlewaretoken
        },
        function (data, status) {
            if (data.status == 'Save') {
                output = '';
                task = data.user_task_list;

                output = show_table(task, output);
                $("#table1").html(output);

            }
        });

}

$(document).ready(function () {
    ajaxcall();


    $('input:radio[type="radio"]').change(function () {

        loading();
        let csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();


        $.post("/task-sort/", 
        {
                sort_by: $('input:radio[name="btnradiob"]:checked').val(),
                order: $('input:radio[name="btnradioa"]:checked').val(),
                csrfmiddlewaretoken: csrfmiddlewaretoken
            },
            function (data, status) {
                if (data.status == 'Save') {
                    output = '';
                    task = data.user_task_list;
                    output = show_table(task, output);
                    setTimeout(function () {
                        $("#table1").html(output);
                    }, 1000);

                }
            });
    });

});
