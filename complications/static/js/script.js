// Генерация fingerprint
FingerprintJS.load()
    .then(fp => fp.get())
    .then(result => {
        const fingerprint = result.visitorId;
        console.log('Fingerprint generated:', fingerprint); // Логирование fingerprint

        // Сохраняем fingerprint на сервере
        axios.post('/save_fingerprint', {
            fingerprint: fingerprint
        })
        .then(response => {
            console.log('Fingerprint saved successfully:', response.data);

            // Загружаем лайки пользователя и инициализируем кнопки
            initializeLikeButtons(fingerprint);
        })
        .catch(error => {
            console.error('Error saving fingerprint:', error);
        });
    })
    .catch(err => {
        console.error('Error generating fingerprint:', err);
    });

// Инициализация кнопок
function initializeLikeButtons(fingerprint) {
    console.log('Initializing like buttons'); // Логирование инициализации кнопок

    const likeButtons = document.querySelectorAll('.like-button');
    console.log('Like buttons found:', likeButtons.length); // Логирование количества кнопок

    // Запрашиваем лайки пользователя
    axios.get('/get_likes', {
        params: {
            fingerprint: fingerprint
        }
    })
    .then(response => {
        console.log('Likes fetched successfully:', response.data); // Логирование полученных лайков
        const likedPresentations = response.data.likedPresentations;

        // Добавляем класс 'liked' к кнопкам, которые пользователь уже лайкнул
        likeButtons.forEach(button => {
            const presentationId = button.getAttribute('id');
            console.log('Button ID:', presentationId); // Логирование ID кнопки

            // Приводим presentationId к строке (если нужно)
            if (likedPresentations.includes(String(presentationId))) {
                button.classList.add('liked');
                console.log('Button already liked:', presentationId); // Логирование уже лайкнутых кнопок
            }
        });

        // Обработчик клика по кнопке
        likeButtons.forEach(button => {
            button.addEventListener('click', () => {
                console.log('Button clicked:', button.getAttribute('id')); // Логирование клика

                const presentationId = button.getAttribute('id');

                if (!button.classList.contains('liked')) {
                    console.log('Sending like request for:', presentationId); // Логирование запроса на лайк

                    // Лайк
                    axios.post('/like', {
                        id: presentationId,
                        fingerprint: fingerprint
                    }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                    .then(response => {
                        console.log('Like successful:', response.data); // Логирование успешного лайка
                        button.classList.add('liked'); // Обновляем состояние кнопки
                    })
                    .catch(error => {
                        console.error('Error details:', error.response ? error.response.data : error.message); // Логирование ошибки
                    });
                } else {
                    console.log('Sending dislike request for:', presentationId); // Логирование запроса на дизлайк

                    // Дизлайк
                    axios.post('/dislike', {
                        id: presentationId,
                        fingerprint: fingerprint
                    }, {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                    .then(response => {
                        console.log('Dislike successful:', response.data); // Логирование успешного дизлайка
                        button.classList.remove('liked'); // Обновляем состояние кнопки
                    })
                    .catch(error => {
                        console.error('Error details:', error.response ? error.response.data : error.message); // Логирование ошибки
                    });
                }
            });
        });
    })
    .catch(error => {
        console.error('Error fetching likes:', error.response ? error.response.data : error.message); // Логирование ошибки при получении лайков
    });
}
