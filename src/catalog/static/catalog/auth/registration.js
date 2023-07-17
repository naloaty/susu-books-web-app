const MDCTextField = mdc.textField.MDCTextField;
const csrfToken = Cookies.get('csrftoken')
axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

class LoginPage {
    constructor() {
        this.login = new MDCTextField(document.querySelector('#login-input').parentNode)
        this.login.error = document.querySelector('#login-input-error')
        this.email = new MDCTextField(document.querySelector('#email-input').parentNode)
        this.email.error = document.querySelector('#email-input-error')
        this.name = new MDCTextField(document.querySelector('#name-input').parentNode)
        this.name.error = document.querySelector('#name-input-error')
        this.password = new MDCTextField(document.querySelector('#password-input').parentNode)
        this.password.error = document.querySelector('#password-input-error')

        this.login.input.addEventListener('blur', () => this.validateLogin())
        this.password.input.addEventListener('input', () => this.validatePassword())
    }

    validateLogin() {
        if (this.login.value.length === 0)
            return

        const data = new FormData();
        data.append('user_login', this.login.value)

        axios.post(api.login.check, data).
        then((response) => {
            const data = response.data;

            if (data.status === 'taken') {
                this.login.valid = false
                this.login.error.innerText = "Этот логин уже занят"
            } else {
                this.login.valid = true
                this.login.error.innerText = ""
            }
        })
    }

    validatePassword() {
        if (this.password.value.length < 6) {
            this.password.valid = false;
            this.password.error.innerText = "Минимальная длина пароля - 6 символов"
        } else {
            this.password.valid = true;
            this.password.error.innerText = ""
        }

    }
}

window.addEventListener("load", () => new LoginPage());
