const validAccount = {
  email: 'user@example.com',
  password: 'StrongPassword123',
  name: 'Career Seeker',
};

function getCurrentUser() {
  try {
    const raw = localStorage.getItem('aiCareerAgentUser');
    return raw ? JSON.parse(raw) : null;
  } catch (error) {
    return null;
  }
}

function setCurrentUser(user) {
  localStorage.setItem('aiCareerAgentUser', JSON.stringify(user));
}

function clearCurrentUser() {
  localStorage.removeItem('aiCareerAgentUser');
}

function initAuth() {
  const form = document.getElementById('auth-form');
  if (!form) return;

  const title = document.getElementById('auth-title');
  const subtitle = document.getElementById('auth-subtitle');
  const submitBtn = document.getElementById('submit-btn');
  const switchLink = document.getElementById('switch-link');
  const switchCopy = document.getElementById('switch-copy');
  const forgotLink = document.getElementById('forgot-link');
  const errorBox = document.getElementById('error');
  const nameGroup = document.getElementById('name-group');
  const confirmGroup = document.getElementById('confirm-group');
  const passwordStrength = document.getElementById('password-strength');
  const modeButtons = document.querySelectorAll('[data-mode]');

  let mode = 'login';

  function showError(message) {
    errorBox.textContent = message;
    errorBox.style.display = 'block';
  }

  function hideError() {
    errorBox.style.display = 'none';
  }

  function evaluatePasswordStrength(password) {
    if (!password) return 'Weak';
    if (password.length < 8) return 'Weak';
    if (/[A-Z]/.test(password) && /[0-9]/.test(password)) return 'Strong';
    return 'Medium';
  }

  function setMode(nextMode) {
    mode = nextMode;
    const isLogin = mode === 'login';

    title.textContent = isLogin ? 'Welcome back' : 'Create your account';
    subtitle.textContent = isLogin
      ? 'Log in to continue your job search and track your next move.'
      : 'Set up your profile and unlock personalized career guidance.';

    submitBtn.textContent = isLogin ? 'Login' : 'Create account';
    nameGroup.classList.toggle('hidden', isLogin);
    confirmGroup.classList.toggle('hidden', isLogin);
    passwordStrength.classList.toggle('hidden', isLogin);
    forgotLink.classList.toggle('hidden', !isLogin);
    switchCopy.textContent = isLogin ? 'Need an account?' : 'Already have an account?';
    switchLink.textContent = isLogin ? 'Create one' : 'Login';

    modeButtons.forEach((button) => {
      button.classList.toggle('active', button.dataset.mode === mode);
    });

    const nameField = document.getElementById('name');
    const confirmField = document.getElementById('confirm-password');
    if (isLogin) {
      nameField.removeAttribute('required');
      confirmField.removeAttribute('required');
    } else {
      nameField.setAttribute('required', 'required');
      confirmField.setAttribute('required', 'required');
    }
  }

  document.getElementById('password').addEventListener('input', function () {
    passwordStrength.textContent = evaluatePasswordStrength(this.value);
    passwordStrength.classList.remove('hidden');
  });

  modeButtons.forEach((button) => {
    button.addEventListener('click', () => setMode(button.dataset.mode));
  });

  switchLink.addEventListener('click', function (event) {
    event.preventDefault();
    setMode(mode === 'login' ? 'register' : 'login');
  });

  forgotLink.addEventListener('click', function (event) {
    event.preventDefault();
    showError('Password reset is available in the full app flow. Demo account: user@example.com');
  });

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    hideError();

    const email = form.email.value.trim();
    const password = form.password.value;

    if (mode === 'register') {
      const name = form.name.value.trim();
      const confirmPassword = form['confirm-password'].value;

      if (!name || !email || !password || !confirmPassword) {
        showError('Please complete all required fields.');
        return;
      }

      if (password.length < 8) {
        showError('Use a password with at least 8 characters.');
        return;
      }

      if (password !== confirmPassword) {
        showError('Passwords do not match.');
        return;
      }

      setCurrentUser({ email, name });
      window.location.href = 'main.html';
      return;
    }

    if (!email || !password) {
      showError('Please enter email and password.');
      return;
    }

    if (email.toLowerCase() === validAccount.email && password === validAccount.password) {
      setCurrentUser({ email: validAccount.email, name: validAccount.name });
      window.location.href = 'main.html';
      return;
    }

    showError('Invalid credentials. Try user@example.com / StrongPassword123.');
  });

  const currentUser = getCurrentUser();
  if (currentUser) {
    window.location.href = 'main.html';
  }

  setMode('login');
}

function initLandingAuthState() {
  const user = getCurrentUser();
  const loginButton = document.getElementById('login-action');
  const logoutButton = document.getElementById('logout-button');
  const heroAction = document.getElementById('hero-action');
  const ctaAction = document.getElementById('cta-action');
  const welcomeText = document.getElementById('welcome-text');

  if (!loginButton || !logoutButton || !heroAction || !ctaAction || !welcomeText) return;

  if (user) {
    loginButton.style.display = 'none';
    logoutButton.style.display = 'inline-flex';
    logoutButton.addEventListener('click', function (event) {
      event.preventDefault();
      clearCurrentUser();
      window.location.reload();
    });
    heroAction.textContent = 'View Your Plan';
    heroAction.href = 'main.html';
    ctaAction.textContent = 'Continue to Dashboard';
    ctaAction.href = 'main.html';
    welcomeText.textContent = 'Welcome back, ' + user.name + '!';
  } else {
    loginButton.style.display = 'inline-flex';
    logoutButton.style.display = 'none';
    heroAction.textContent = 'Start Free';
    heroAction.href = 'loginpage.html';
    ctaAction.textContent = 'Create Your Free Account';
    ctaAction.href = 'loginpage.html';
    welcomeText.textContent = 'Smart career help for ambitious professionals';
  }
}

document.addEventListener('DOMContentLoaded', function () {
  initAuth();
  initLandingAuthState();
});
