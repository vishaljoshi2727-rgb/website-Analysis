async function analyzeWebsite(){

    const url = document.getElementById("websiteUrl").value;

    const loader = document.getElementById("loader");

    const result = document.getElementById("result");

    loader.classList.remove("hidden");

    result.classList.add("hidden");

    try{

        const response = await fetch("/analyze",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                url:url
            })

        });

        const data = await response.json();

        loader.classList.add("hidden");

        if(data.error){

            alert(data.error);
            return;
        }

        result.classList.remove("hidden");

        document.getElementById("website_type").innerText =
            data.website_type;

        document.getElementById("title").innerText =
            data.title;

        document.getElementById("meta_description").innerText =
            data.meta_description;

        document.getElementById("tone").innerText =
            data.tone;

        document.getElementById("links").innerText =
            data.links;

        document.getElementById("images").innerText =
            data.images;

        document.getElementById("forms").innerText =
            data.forms;

        document.getElementById("preview").innerText =
            data.preview;

        document.getElementById("conclusion").innerText =
            data.conclusion;

    }
    catch(error){

        loader.classList.add("hidden");

        alert("Error analyzing website");
    }
}