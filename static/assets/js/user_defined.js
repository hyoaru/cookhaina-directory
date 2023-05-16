function removePlaceholder(mealCardID) {
    card = document.querySelector(`#mealCard-${mealCardID}`);
    const mealCardImageContainer = card.firstElementChild;
    const mealCardImage = mealCardImageContainer.lastElementChild;
    const mealCardTitle = card.lastElementChild.firstElementChild;

    mealCardImageContainer.children[0].remove();
    mealCardImageContainer.children[0].remove();
    mealCardImage.classList.remove('d-none');
    mealCardTitle.classList.remove('placeholder');
}

document.querySelectorAll('.meal-card').forEach((card) => {
    const mealCardImageContainer = card.firstElementChild;
    const mealCardImage = mealCardImageContainer.lastElementChild;
    const mealCardTitle = card.lastElementChild.firstElementChild;

    card.style.transition = "all 0.3s"

    card.addEventListener('mouseover', () => {
        if (!card.classList.contains('border-primary')){
            card.classList.add('border-primary')
            card.style.transform = 'scale(1.02)'
        }
    })

    card.addEventListener('mouseout', () => {
        if (card.classList.contains('border-primary')){
            card.classList.remove('border-primary')
            card.style.transform = 'scale(1)'
        }
    })
})


document.querySelector('#categoryButton').addEventListener('click', () => {
    const categoryButton = document.querySelector('#categoryButton');
    if (categoryButton.classList.contains('collapsed')) {
        categoryButton.style.transition = "all 3s"
    } else {
        categoryButton.style.transition = "all 0s"
    }
    categoryButton.classList.toggle('rounded-bottom-0')
})

document.querySelectorAll('.category-pill').forEach((pill) => {

    pill.style.transition = "all 0.3s"

    pill.addEventListener('mouseover', () => {
        pill.classList.toggle('text-bg-white')
        pill.classList.toggle('text-bg-primary')
    })

    pill.addEventListener('mouseout', () => {
        pill.classList.toggle('text-bg-white')
        pill.classList.toggle('text-bg-primary')
    })
})

function openLink(link) {
    window.location.href = link;
    console.log(link)
}