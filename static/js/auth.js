// Firebase configuration for your project
const firebaseConfig = {
    apiKey: "AIzaSyARsUQe9N6CfOzXaa02HhkYBrhQ2ngWjRU",
    authDomain: "webbuilder-6f7f3.firebaseapp.com",
    projectId: "webbuilder-6f7f3",
    storageBucket: "webbuilder-6f7f3.firebasestorage.app",
    messagingSenderId: "980941820475",
    appId: "1:980941820475:web:787458a6acce3d3c94821e",
    measurementId: "G-VD9JF734GZ"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.firestore();

// DOM elements
const loginForm = document.getElementById('loginForm');
const signupForm = document.getElementById('signupForm');
const showSignup = document.getElementById('showSignup');
const showLogin = document.getElementById('showLogin');
const loginFormElement = document.getElementById('loginFormElement');
const signupFormElement = document.getElementById('signupFormElement');
const googleLoginBtn = document.getElementById('googleLoginBtn');
const googleSignupBtn = document.getElementById('googleSignupBtn');

// Form switching
if (showSignup) {
    showSignup.addEventListener('click', (e) => {
        e.preventDefault();
        loginForm.style.display = 'none';
        signupForm.style.display = 'block';
        console.log('📱 Switched to signup form');
    });
}

if (showLogin) {
    showLogin.addEventListener('click', (e) => {
        e.preventDefault();
        signupForm.style.display = 'none';
        loginForm.style.display = 'block';
        console.log('📱 Switched to login form');
    });
}

// Login form submission
if (loginFormElement) {
    loginFormElement.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        
        if (!email || !password) {
            alert('Please fill in all fields.');
            return;
        }
        
        try {
            const submitBtn = e.target.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Signing in...';
            
            console.log('🔐 Attempting login for:', email);
            
            await auth.signInWithEmailAndPassword(email, password);
            console.log('✅ Login successful');
            window.location.href = '/dashboard';
        } catch (error) {
            console.error('❌ Login failed:', error);
            alert('Login failed: ' + error.message);
            const submitBtn = e.target.querySelector('button[type="submit"]');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Sign In';
        }
    });
}

// Signup form submission
if (signupFormElement) {
    signupFormElement.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const name = document.getElementById('signupName').value;
        const email = document.getElementById('signupEmail').value;
        const password = document.getElementById('signupPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (!name || !email || !password || !confirmPassword) {
            alert('Please fill in all fields.');
            return;
        }
        
        if (password !== confirmPassword) {
            alert('Passwords do not match.');
            return;
        }
        
        if (password.length < 6) {
            alert('Password must be at least 6 characters long.');
            return;
        }
        
        try {
            const submitBtn = e.target.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Creating account...';
            
            console.log('📝 Attempting signup for:', email);
            
            const userCredential = await auth.createUserWithEmailAndPassword(email, password);
            
            // Update profile with display name
            await userCredential.user.updateProfile({
                displayName: name
            });
            
            // Save user data to Firestore
            await db.collection('users').doc(userCredential.user.uid).set({
                name: name,
                email: email,
                createdAt: firebase.firestore.FieldValue.serverTimestamp(),
                settings: {
                    emailNotifications: true,
                    darkMode: false,
                    autoSave: true,
                    defaultPrivacy: 'private'
                },
                profileComplete: true
            });
            
            console.log('✅ Signup successful');
            window.location.href = '/dashboard';
        } catch (error) {
            console.error('❌ Signup failed:', error);
            alert('Signup failed: ' + error.message);
            const submitBtn = e.target.querySelector('button[type="submit"]');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Create Account';
        }
    });
}

// Google authentication
const googleProvider = new firebase.auth.GoogleAuthProvider();

if (googleLoginBtn) {
    googleLoginBtn.addEventListener('click', async () => {
        try {
            googleLoginBtn.disabled = true;
            googleLoginBtn.innerHTML = '<i class="fab fa-google"></i> Signing in...';
            
            console.log('🔐 Attempting Google login');
            
            const result = await auth.signInWithPopup(googleProvider);
            
            // Save user data to Firestore if new user
            const userDoc = await db.collection('users').doc(result.user.uid).get();
            if (!userDoc.exists) {
                await db.collection('users').doc(result.user.uid).set({
                    name: result.user.displayName,
                    email: result.user.email,
                    createdAt: firebase.firestore.FieldValue.serverTimestamp(),
                    settings: {
                        emailNotifications: true,
                        darkMode: false,
                        autoSave: true,
                        defaultPrivacy: 'private'
                    },
                    profileComplete: true
                });
            }
            
            console.log('✅ Google login successful');
            window.location.href = '/dashboard';
        } catch (error) {
            console.error('❌ Google login failed:', error);
            alert('Google login failed: ' + error.message);
            googleLoginBtn.disabled = false;
            googleLoginBtn.innerHTML = '<i class="fab fa-google"></i> Continue with Google';
        }
    });
}

if (googleSignupBtn) {
    googleSignupBtn.addEventListener('click', async () => {
        try {
            googleSignupBtn.disabled = true;
            googleSignupBtn.innerHTML = '<i class="fab fa-google"></i> Creating account...';
            
            console.log('📝 Attempting Google signup');
            
            const result = await auth.signInWithPopup(googleProvider);
            
            // Save user data to Firestore
            await db.collection('users').doc(result.user.uid).set({
                name: result.user.displayName,
                email: result.user.email,
                createdAt: firebase.firestore.FieldValue.serverTimestamp(),
                settings: {
                    emailNotifications: true,
                    darkMode: false,
                    autoSave: true,
                    defaultPrivacy: 'private'
                },
                profileComplete: true
            });
            
            console.log('✅ Google signup successful');
            window.location.href = '/dashboard';
        } catch (error) {
            console.error('❌ Google signup failed:', error);
            alert('Google signup failed: ' + error.message);
            googleSignupBtn.disabled = false;
            googleSignupBtn.innerHTML = '<i class="fab fa-google"></i> Continue with Google';
        }
    });
}

// Check if user is already logged in
auth.onAuthStateChanged((user) => {
    if (user) {
        console.log('👤 User already logged in, redirecting to dashboard');
        window.location.href = '/dashboard';
    } else {
        console.log('👤 No user logged in');
    }
});

// Initialize auth page
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Auth.js initialized');
});
