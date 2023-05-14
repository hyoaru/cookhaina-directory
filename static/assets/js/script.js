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