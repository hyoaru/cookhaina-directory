const mealCard = document.querySelectorAll('.meal-card')
const categoryButton = document.querySelector('#categoryButton');


mealCard.forEach((card) => {
    const mealCardImageContainer = card.firstElementChild;
    const mealCardImage = mealCardImageContainer.lastElementChild;
    const mealCardTitle = card.lastElementChild.firstElementChild;

    mealCardImage.addEventListener('load', () => {
        mealCardImageContainer.children[0].remove();
        mealCardImageContainer.children[0].remove();
        mealCardImage.classList.remove('d-none');
        mealCardTitle.classList.remove('placeholder');
    })

    card.style.transition = "all 0.5s"

    card.addEventListener('mouseover', () => {
        card.classList.toggle('border-primary')
        card.style.transform = 'scale(1.02)'
    })

    card.addEventListener('mouseout', () => {
        card.classList.toggle('border-primary')
        card.style.transform = 'scale(1)'
    })
})


categoryButton.addEventListener('click', () => {
    console.log(categoryButton.attributes)
    if (categoryButton.classList.contains('rounded-bottom-0')) {
        categoryButton.style.transition = "all 3s"
    } else {
        categoryButton.style.transition = "all 0s"
    }
    categoryButton.classList.toggle('rounded-bottom-0')
})