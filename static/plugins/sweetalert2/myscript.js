// logout-notifikasi
$('.logout-notif').on('click', function (e) {

    // e = event
    // mematikan funtion href yang seharusnya berjalan jika di klick
    e.preventDefault();

    //var href 
    const href = $(this).attr('href');

    Swal.fire({
        title: 'Are you sure',
        text: "Want to logout network automation?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Logout'
    }).then((result) => {
        if (result.isConfirmed) {
            document.location.href = href;
            Swal.fire(
                'Logout!',
                'Success logout from network automation',
                'success'
            )
        }
    })

});



// tombol delete user
$('.delete-user').on('click', function(e){

    // e = event
    // mematikan funtion href yang seharusnya berjalan jika di klick
    e.preventDefault();
    
    //var href 
    const href = $(this).attr('href');

    Swal.fire({
                title: 'Are you sure?',
                text: "Want to delete this user data?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Delete User!'
            }).then((result) => {
            if (result.isConfirmed) {
                document.location.href = href;
                Swal.fire(
                'Delete!',
                'Data has been deleted.',
                'success'
                )
            }
            })

});


// tombol delete groups
$('.delete-group').on('click', function (e) {

    // e = event
    // mematikan funtion href yang seharusnya berjalan jika di klick
    e.preventDefault();

    //var href 
    const href = $(this).attr('href');

    Swal.fire({
        title: 'Are you sure?',
        text: "Want to delete this group data?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Delete Group!'
    }).then((result) => {
        if (result.isConfirmed) {
            document.location.href = href;
            Swal.fire(
                'Delete!',
                'Data has been deleted.',
                'success'
            )
        }
    })

});

// tombol delete permissions
$('.delete-permissions').on('click', function (e) {

    // e = event
    // mematikan funtion href yang seharusnya berjalan jika di klick
    e.preventDefault();

    //var href 
    const href = $(this).attr('href');

    Swal.fire({
        title: 'Are you sure?',
        text: "Want to delete this permission data?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Delete Permission!'
    }).then((result) => {
        if (result.isConfirmed) {
            document.location.href = href;
            Swal.fire(
                'Delete!',
                'Data has been deleted.',
                'success'
            )
        }
    })

});


// tombol delete permissions
$('.delete-role').on('click', function (e) {

    // e = event
    // mematikan funtion href yang seharusnya berjalan jika di klick
    e.preventDefault();

    //var href 
    const href = $(this).attr('href');

    Swal.fire({
        title: 'Are you sure?',
        text: "Want to delete this role data?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Delete Role!'
    }).then((result) => {
        if (result.isConfirmed) {
            document.location.href = href;
            Swal.fire(
                'Delete!',
                'Data has been deleted.',
                'success'
            )
        }
    })

});



// start container
$('.start-container').on('click', function (e) {

    // e = event
    // mematikan funtion href yang seharusnya berjalan jika di klick
    e.preventDefault();

    //var href 
    const href = $(this).attr('href');

    Swal.fire({
        title: 'Are you sure',
        text: "Want to start this container?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#1CBB8C',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Start Container!'
    }).then((result) => {
        if (result.isConfirmed) {
            document.location.href = href;
            Swal.fire(
                'Start!',
                'Success start container',
                'success'
            )
        }
    })

});

// stop container
$('.stop-container').on('click', function (e) {

    // e = event
    // mematikan funtion href yang seharusnya berjalan jika di klick
    e.preventDefault();

    //var href 
    const href = $(this).attr('href');

    Swal.fire({
        title: 'Are you sure',
        text: "Want to stop this container?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#FCB92C',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Stop Container!'
    }).then((result) => {
        if (result.isConfirmed) {
            document.location.href = href;
            Swal.fire(
                'Stop!',
                'Success stop container',
                'success'
            )
        }
    })

});


// reboot container
$('.reboot-container').on('click', function (e) {

    // e = event
    // mematikan funtion href yang seharusnya berjalan jika di klick
    e.preventDefault();

    //var href 
    const href = $(this).attr('href');

    Swal.fire({
        title: 'Are you sure?',
        text: "Want to reboot this container?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Reboot Container!'
    }).then((result) => {
        if (result.isConfirmed) {
            document.location.href = href;
            Swal.fire(
                'Reboot!',
                'Success reboot container',
                'success'
            )
        }
    })

});

// remove container
$('.remove-container').on('click', function (e) {

    // e = event
    // mematikan funtion href yang seharusnya berjalan jika di klick
    e.preventDefault();

    //var href 
    const href = $(this).attr('href');

    Swal.fire({
        title: 'Are you sure?',
        text: "Want to remove this container?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Remove Container!'
    }).then((result) => {
        if (result.isConfirmed) {
            document.location.href = href;
            Swal.fire(
                'Remove!',
                'Success remove container',
                'success'
            )
        }
    })

});


// start virtual machine
$('.start-virtual_machine').on('click', function (e) {

    // e = event
    // mematikan funtion href yang seharusnya berjalan jika di klick
    e.preventDefault();

    //var href 
    const href = $(this).attr('href');

    Swal.fire({
        title: 'Are you sure',
        text: "Want to start this virtual machine?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#1CBB8C',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Start VM!'
    }).then((result) => {
        if (result.isConfirmed) {
            document.location.href = href;
            Swal.fire(
                'Start!',
                'Success start virtual machine',
                'success'
            )
        }
    })

});

// stop virtual machine
$('.stop-virtual_machine').on('click', function (e) {

    // e = event
    // mematikan funtion href yang seharusnya berjalan jika di klick
    e.preventDefault();

    //var href 
    const href = $(this).attr('href');

    Swal.fire({
        title: 'Are you sure',
        text: "Want to stop this virtual machine?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#FCB92C',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Stop VM!'
    }).then((result) => {
        if (result.isConfirmed) {
            document.location.href = href;
            Swal.fire(
                'Stop!',
                'Success stop virtual machine',
                'success'
            )
        }
    })

});


// reboot virtual machine
$('.reboot-virtual_machine').on('click', function (e) {

    // e = event
    // mematikan funtion href yang seharusnya berjalan jika di klick
    e.preventDefault();

    //var href 
    const href = $(this).attr('href');

    Swal.fire({
        title: 'Are you sure?',
        text: "Want to reboot this virtual machine?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Reboot VM!'
    }).then((result) => {
        if (result.isConfirmed) {
            document.location.href = href;
            Swal.fire(
                'Reboot!',
                'Success reboot virtual machine',
                'success'
            )
        }
    })

});

// remove virtual machine
$('.remove-virtual_machine').on('click', function (e) {

    // e = event
    // mematikan funtion href yang seharusnya berjalan jika di klick
    e.preventDefault();

    //var href 
    const href = $(this).attr('href');

    Swal.fire({
        title: 'Are you sure?',
        text: "Want to remove this virtual machine?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Remove VM!'
    }).then((result) => {
        if (result.isConfirmed) {
            document.location.href = href;
            Swal.fire(
                'Remove!',
                'Success remove virtual machine',
                'success'
            )
        }
    })

});









// $('.notif').on('click', function(e){
//     Swal.fire({
//         title: 'Custom animation with Animate.css',
//         showClass: {
//         popup: 'animate__animated animate__fadeInDown'
//         },
//         hideClass: {
//         popup: 'animate__animated animate__fadeOutUp'}
// })
// });


// let table = new DataTable('#myTable');


// new DataTable('#dataTable');
// $('#dataTable').DataTable( {
//     // paging: false,
//     // scrollY: 400
// } );


// $(document).ready(function() {
//     $('#akunGuru').DataTable( {
//         "language": {
//                         "search": "Cari:",
//                         "lengthMenu": "Menampilkan _MENU_ data",
//                         "info": "Menampilkan _START_ sampai _END_ data dari _TOTAL_ data",
//                         "infoEmpty": "Tidak ada data yang ditampilkan",
//                         "infoFiltered": "(dari total _MAX_ data)",
//                         "zeroRecords": "Tidak ada hasil pencarian ditemukan",
//                         "paginate": {
//                             "first": "&laquo;",
//                             "last": "&raquo;",
//                             "next": "&rsaquo;",
//                             "previous": "&lsaquo;"
//                         }
//                     }
//     } );
// } );











