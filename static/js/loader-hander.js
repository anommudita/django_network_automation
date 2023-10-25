const loaderEnd = () => {
    const loader = document.querySelector('#loader');

    // css loadng animation
    const loading = loader.querySelector('div');
    // const img = loader.querySelector('img');
    document.body.classList.remove('vh-100');
    document.body.classList.remove('vw-100');
    document.body.classList.remove('overflow-hidden');;
    loading.style.transform = "scale(2)";
    loader.style.opacity = "0";
    console.log("yes")
    setTimeout((() => {
        loader.classList.add('d-none');
        loader.remove();
        console.log("yes")  
    }), 1400)

}


// animasi loading fix
window.addEventListener("load", () => {
    // console.log("yes1");

    var container = document.getElementById("loader");

    container.classList.add("end-loading");
})

