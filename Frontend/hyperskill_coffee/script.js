function addReview(event) {
    event.preventDefault();
    let reviews = document.getElementById("reviewsRow");

    let title = document.getElementById("reviewTitle").value;
    let text = document.getElementById("reviewText").value;
    let name = document.getElementById("reviewName").value;

    const review = `<div class="col-lg-4 col-md-6 py-3">
                        <div class="card h-100">
                            <div class="card-body">
                                <h4 class="card-title">${title}</h4>
                                <blockquote class="blockquote mb-0">
                                    <p>${text}</p>
                                    <footer class="text-end blockquote-footer"><i>${name || "Anonymous"}</i></footer>
                                </blockquote>
                            </div>
                        </div>
                    </div>`;

    reviews.innerHTML += review;
}

const form = document.getElementById('reviewButton');
form.addEventListener('click', addReview);
