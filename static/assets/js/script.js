document.querySelectorAll('.meal-card').forEach((mealCard) => {
    const mealCardImageContainer = mealCard.firstElementChild;
    const mealCardImage = mealCardImageContainer.lastElementChild;
    const mealCardTitle = mealCard.lastElementChild.firstElementChild;
    mealCardImage.addEventListener('load', () => {
        mealCardImageContainer.children[0].remove();
        mealCardImageContainer.children[0].remove();
        mealCardImage.classList.remove('d-none');
        mealCardTitle.classList.remove('placeholder');
    })
})

const categoryButton = document.querySelector('#categoryButton');

categoryButton.addEventListener('click', () => {

    console.log(categoryButton.attributes)
    if (categoryButton.classList.contains('rounded-bottom-0')) {
        categoryButton.style.transition = "all 3s"
    } else {
        categoryButton.style.transition = "all 0s"
    }
    categoryButton.classList.toggle('rounded-bottom-0')
})