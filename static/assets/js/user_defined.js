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

function setMealCardEffects() {
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
}


function setCategoryEffects() {
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
}

function openLink(link) {
    window.location.href = link;
}

function setMealInstructionsEffects() {
    const instructionBody = document.querySelector('#instructionBody');
    const instructionToggle1 = document.querySelector('#instructionToggle1');
    const instructionToggle2 = document.querySelector('#instructionToggle2');

    function toggleVisibilityInstructionToggle1() {
        if (instructionToggle2.classList.contains('collapsed')) {
            setTimeout(() => {
                instructionToggle1.classList.remove('d-none');
            }, 225)
        } else {
            instructionToggle1.classList.add('d-none');
        }
    }

    instructionToggle1.addEventListener('click', () => {
        toggleVisibilityInstructionToggle1();
    })

    instructionToggle2.addEventListener('click', () => {
        toggleVisibilityInstructionToggle1();
    })
}

function setMealThumbnailEffects() {
    const mealThumbnailContainers = document.querySelectorAll('.mealThumbnailContainer');
    const mealThumbnailSeeVideoIndicators = document.querySelectorAll('.mealThumbnailSeeVideoIndicator');

    mealThumbnailContainers.forEach((mealThumbnailContainer) => {
        mealThumbnailContainer.addEventListener('mouseover', () => {
            mealThumbnailSeeVideoIndicators.forEach((mealThumbnailSeeVideoIndicator) => {
                mealThumbnailSeeVideoIndicator.classList.remove('d-none')
                mealThumbnailSeeVideoIndicator.classList.add('animate__fadeIn')
                mealThumbnailSeeVideoIndicator.classList.remove('animate__fadeOut')
            })
        })
    })

    mealThumbnailContainers.forEach((mealThumbnailContainer) => {
        mealThumbnailContainer.addEventListener('mouseout', () => {
            mealThumbnailSeeVideoIndicators.forEach((mealThumbnailSeeVideoIndicator) => {
                mealThumbnailSeeVideoIndicator.classList.remove('animate__fadeIn')
                mealThumbnailSeeVideoIndicator.classList.add('animate__fadeOut')
            })
        })
    })

}