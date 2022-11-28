function sendCurrentCity() {
    const domain = window.location.host
    let citySelector = null;
    try {
        citySelector = document.getElementById('cities');
        console.log(cities);
    } catch {
        console.log('Error');
    }
    if (citySelector) {
        console.log("CITY");
        citySelector.addEventListener('change', (e) => {
            console.log("CHANGED")
            const postSelect = document.querySelector('#posts')
            const allPosts = postSelect.querySelectorAll('option')
            for (post of allPosts) {
                post.remove()
            }
            let selectedCity = citySelector.options[citySelector.selectedIndex].text
            console.log(typeof selectedCity)


            const token = document.cookie
                .split('; ')
                .find((row) => row.startsWith('csrftoken='))
                ?.split('=')[1];
            console.log(token);
            console.log(domain);
            url = `http://${domain}/test_process/`;
            console.log(url);
            fetch(`http://${domain}/test_process/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': token,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'city': selectedCity })
            })
                .then(response => response.json())
                .then(data => {
                    let posts = data
                    const noNeedPost = postSelect.firstElementChild
                    console.log(typeof posts)
                    for (i of posts) {
                        console.log(i + "\n")
                        const newPost = document.createElement("option")
                        newPost.text = i
                        postSelect.add(newPost)
                    }

                    console.log(postSelect)
                    console.log(noNeedPost)
                    try {
                        if (postSelect.firstElementChild.text == 'Спочатку оберіть місто') {
                            postSelect.firstElementChild.remove()
                        }
                    } catch {
                        console.log('NOTHING')
                    }

                    if (!(postSelect.firstElementChild)) {
                        const emptyPost = document.createElement("option")
                        emptyPost.text = 'Немає працюючих відділень!'
                        postSelect.add(emptyPost)
                    }

                })





            // var xhr = new XMLHttpRequest();
            // xhr.open("POST", `http://${domain}/goods_processing/`, true);
            // xhr.setRequestHeader('X-CSRFToken', token);
            // xhr.send(JSON.stringify({ 'city': 'dsfds' }));

            // let data = new FormData();
            // data.append("city", selectedCity)
            // data.append("csrfmiddlewaretoken", token)
            // axios.post(`http://${domain}/test_process/`, data)
        })

    } else {
        console.log("NOT CITY");
    }

}

sendCurrentCity();