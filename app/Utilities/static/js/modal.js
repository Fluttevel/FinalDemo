const modal = document.querySelector('.modal')
const openModalButton = document.querySelector('.open-modal')
const closeModalButton = document.querySelector('.modal__close')


openModalButton.addEventListener('click', e =>
{
    e.preventDefault()

    modal.classList.add('modal--open')
})

closeModalButton.addEventListener('click', e =>
{
    e.preventDefault()

    modal.classList.remove('modal--open')
})
