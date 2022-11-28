function sendCurrentCity() {
    const domain = window.location.host
    let citySelector = null;
    try {
        citySelector = document.getElementById('cities');
    } catch {
        console.log('Error');
    }
    if (citySelector) {
        citySelector.addEventListener('change', (e) => {
            const postSelect = document.querySelector('#posts')
            const allPosts = postSelect.querySelectorAll('option')
            // remove all posts from previous choices
            for (post of allPosts) {
                post.remove()
            }
            // get city name and token
            let selectedCity = citySelector.options[citySelector.selectedIndex].text
            const token = document.cookie
                .split('; ')
                .find((row) => row.startsWith('csrftoken='))
                ?.split('=')[1];
            // Sending POST request to django
            fetch(`https://${domain}/test_process/`, {
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
                    // Add mail posts to select list
                    for (i of posts) {
                        const newPost = document.createElement("option")
                        newPost.text = i
                        postSelect.add(newPost)
                    }

                    // Removing warning option
                    try {
                        if (postSelect.firstElementChild.text == 'Спочатку оберіть місто') {
                            postSelect.firstElementChild.remove()
                        }
                    } catch {
                        console.log('No posts here')
                    }

                    // Add info about not existing posts
                    if (!(postSelect.firstElementChild)) {
                        const emptyPost = document.createElement("option")
                        emptyPost.text = 'Немає працюючих відділень!'
                        postSelect.add(emptyPost)
                    }
                })
        })

    } else {
        console.log("NOT CITY");
    }

}

sendCurrentCity();