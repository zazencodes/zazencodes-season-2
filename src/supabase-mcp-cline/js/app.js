// Initialize Supabase client
const supabaseUrl = SUPABASE_CONFIG.url;
const supabaseKey = SUPABASE_CONFIG.anonKey;
const supabase = window.supabase.createClient(supabaseUrl, supabaseKey);

// DOM Elements
const canvas = document.getElementById('wallpaper-canvas');
const ctx = canvas.getContext('2d');
const resolutionSelect = document.getElementById('resolution');
const widthInput = document.getElementById('width');
const heightInput = document.getElementById('height');
const customResolution = document.querySelector('.custom-resolution');
const styleSelect = document.getElementById('style');
const color1Input = document.getElementById('color1');
const color2Input = document.getElementById('color2');
const colorModeSelect = document.getElementById('color-mode');
const opacityInput = document.getElementById('opacity');
const opacityValue = document.getElementById('opacity-value');
const blurInput = document.getElementById('blur');
const blurValue = document.getElementById('blur-value');
const generateBtn = document.getElementById('generate-btn');
const saveBtn = document.getElementById('save-btn');
const downloadBtn = document.getElementById('download-btn');
const galleryContainer = document.getElementById('gallery');
const authContainer = document.getElementById('auth-container');
const signinBtn = document.getElementById('signin-btn');
const signupBtn = document.getElementById('signup-btn');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');

// AI Image Generation Elements
const aiControls = document.querySelector('.ai-controls');
const aiPromptInput = document.getElementById('ai-prompt');
const generateAiBtn = document.getElementById('generate-ai-btn');
const aiLoading = document.getElementById('ai-loading');

// State
let currentUser = null;
let currentWallpaper = null;
let particles = [];
let animationFrameId = null;

// Initialize the application
function init() {
    // Set canvas size based on default resolution
    setCanvasSize('1920x1080');
    
    // Add event listeners
    resolutionSelect.addEventListener('change', handleResolutionChange);
    widthInput.addEventListener('change', updateCustomResolution);
    heightInput.addEventListener('change', updateCustomResolution);
    opacityInput.addEventListener('input', updateOpacityValue);
    blurInput.addEventListener('input', updateBlurValue);
    generateBtn.addEventListener('click', generateWallpaper);
    saveBtn.addEventListener('click', saveWallpaper);
    downloadBtn.addEventListener('click', downloadWallpaper);
    signinBtn.addEventListener('click', handleSignIn);
    signupBtn.addEventListener('click', handleSignUp);
    styleSelect.addEventListener('change', handleStyleChange);
    generateAiBtn.addEventListener('click', generateAiWallpaper);
    
    // Check if user is already logged in
    checkAuthState();
    
    // Generate initial wallpaper
    generateWallpaper();
}

// Handle style change
function handleStyleChange() {
    const style = styleSelect.value;
    
    // Show/hide AI controls based on selected style
    if (style === 'ai-generated') {
        aiControls.style.display = 'block';
    } else {
        aiControls.style.display = 'none';
        generateWallpaper();
    }
}

// Generate AI wallpaper
async function generateAiWallpaper() {
    const prompt = aiPromptInput.value.trim();
    
    if (!prompt) {
        alert('Please enter a description for your wallpaper');
        return;
    }
    
    try {
        // Show loading indicator
        aiLoading.style.display = 'flex';
        generateAiBtn.disabled = true;
        
        // Get canvas dimensions
        const width = canvas.width;
        const height = canvas.height;
        
        // Determine the best size for the image based on canvas dimensions
        // OpenAI supports square images, so we'll use the largest dimension
        const maxDimension = Math.max(width, height);
        let imageSize = '1024x1024'; // Default size
        
        if (maxDimension <= 512) {
            imageSize = '512x512';
        } else if (maxDimension <= 1024) {
            imageSize = '1024x1024';
        } else {
            imageSize = '1792x1024'; // For wider wallpapers
        }
        
        // Call Supabase Edge Function to generate image
        const { data: functionData, error: functionError } = await supabase.functions.invoke('generate-image', {
            body: {
                prompt: prompt,
                size: imageSize,
                quality: 'hd',
                style: 'natural'
            }
        });
        
        if (functionError) {
            throw new Error(functionError.message || 'Failed to generate image');
        }
        
        if (!functionData || !functionData.data || !functionData.data[0] || !functionData.data[0].url) {
            throw new Error('Invalid response from image generation service');
        }
        
        const imageUrl = functionData.data[0].url;
        
        // Load the generated image onto the canvas
        const img = new Image();
        img.crossOrigin = 'Anonymous';
        
        img.onload = function() {
            // Clear canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Draw image on canvas, centered and scaled to fit
            const aspectRatio = img.width / img.height;
            let drawWidth, drawHeight, drawX, drawY;
            
            if (canvas.width / canvas.height > aspectRatio) {
                // Canvas is wider than image
                drawHeight = canvas.height;
                drawWidth = drawHeight * aspectRatio;
                drawX = (canvas.width - drawWidth) / 2;
                drawY = 0;
            } else {
                // Canvas is taller than image
                drawWidth = canvas.width;
                drawHeight = drawWidth / aspectRatio;
                drawX = 0;
                drawY = (canvas.height - drawHeight) / 2;
            }
            
            ctx.drawImage(img, drawX, drawY, drawWidth, drawHeight);
            
            // Save current wallpaper data
            currentWallpaper = {
                style: 'ai-generated',
                prompt: prompt,
                width: canvas.width,
                height: canvas.height,
                dataUrl: canvas.toDataURL('image/png')
            };
            
            // Hide loading indicator
            aiLoading.style.display = 'none';
            generateAiBtn.disabled = false;
        };
        
        img.onerror = function() {
            console.error('Error loading generated image');
            alert('Failed to load the generated image. Please try again.');
            aiLoading.style.display = 'none';
            generateAiBtn.disabled = false;
        };
        
        img.src = imageUrl;
        
    } catch (error) {
        console.error('Error generating AI image:', error);
        alert('Failed to generate image: ' + error.message);
        aiLoading.style.display = 'none';
        generateAiBtn.disabled = false;
    }
}

// Set canvas size based on selected resolution
function setCanvasSize(resolution) {
    if (resolution === 'custom') {
        canvas.width = parseInt(widthInput.value);
        canvas.height = parseInt(heightInput.value);
    } else {
        const [width, height] = resolution.split('x');
        canvas.width = parseInt(width);
        canvas.height = parseInt(height);
    }
    
    // Adjust canvas display size for preview
    const maxWidth = 800;
    const maxHeight = 500;
    const aspectRatio = canvas.width / canvas.height;
    
    if (aspectRatio > maxWidth / maxHeight) {
        canvas.style.width = maxWidth + 'px';
        canvas.style.height = (maxWidth / aspectRatio) + 'px';
    } else {
        canvas.style.height = maxHeight + 'px';
        canvas.style.width = (maxHeight * aspectRatio) + 'px';
    }
}

// Handle resolution change
function handleResolutionChange() {
    const resolution = resolutionSelect.value;
    
    if (resolution === 'custom') {
        customResolution.style.display = 'block';
    } else {
        customResolution.style.display = 'none';
        setCanvasSize(resolution);
        generateWallpaper();
    }
}

// Update canvas size for custom resolution
function updateCustomResolution() {
    if (resolutionSelect.value === 'custom') {
        setCanvasSize('custom');
        generateWallpaper();
    }
}

// Update opacity value display
function updateOpacityValue() {
    opacityValue.textContent = opacityInput.value + '%';
    generateWallpaper();
}

// Update blur value display
function updateBlurValue() {
    blurValue.textContent = blurInput.value + 'px';
    generateWallpaper();
}

// Generate wallpaper based on selected options
function generateWallpaper() {
    // Cancel any ongoing animation
    if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
        animationFrameId = null;
    }
    
    const style = styleSelect.value;
    const color1 = color1Input.value;
    const color2 = color2Input.value;
    const colorMode = colorModeSelect.value;
    const opacity = opacityInput.value / 100;
    const blur = parseInt(blurInput.value);
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Apply global settings
    ctx.globalAlpha = opacity;
    
    // Generate wallpaper based on selected style
    switch (style) {
        case 'gradient':
            generateGradient(color1, color2, colorMode);
            break;
        case 'geometric':
            generateGeometric(color1, color2, colorMode);
            break;
        case 'particles':
            generateParticles(color1, color2, colorMode);
            break;
        case 'waves':
            generateWaves(color1, color2, colorMode);
            break;
    }
    
    // Apply blur if needed
    if (blur > 0) {
        // Note: Canvas blur is not directly supported
        // This is a visual approximation using CSS
        canvas.style.filter = `blur(${blur}px)`;
    } else {
        canvas.style.filter = 'none';
    }
    
    // Save current wallpaper data
    currentWallpaper = {
        style,
        color1,
        color2,
        colorMode,
        opacity: opacityInput.value,
        blur,
        width: canvas.width,
        height: canvas.height,
        dataUrl: canvas.toDataURL('image/png')
    };
}

// Generate gradient wallpaper
function generateGradient(color1, color2, colorMode) {
    let gradient;
    
    // Random angle for gradient
    const angle = colorMode === 'random' ? Math.random() * 360 : 45;
    const angleRad = (angle * Math.PI) / 180;
    
    // Calculate gradient start and end points
    const x1 = canvas.width / 2 - Math.cos(angleRad) * canvas.width;
    const y1 = canvas.height / 2 - Math.sin(angleRad) * canvas.height;
    const x2 = canvas.width / 2 + Math.cos(angleRad) * canvas.width;
    const y2 = canvas.height / 2 + Math.sin(angleRad) * canvas.height;
    
    gradient = ctx.createLinearGradient(x1, y1, x2, y2);
    
    if (colorMode === 'random') {
        // Generate random colors for gradient stops
        for (let i = 0; i < 5; i++) {
            const randomColor = getRandomColor();
            gradient.addColorStop(i / 4, randomColor);
        }
    } else {
        gradient.addColorStop(0, color1);
        gradient.addColorStop(1, color2);
    }
    
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

// Generate geometric wallpaper
function generateGeometric(color1, color2, colorMode) {
    // Fill background
    ctx.fillStyle = color1;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Number of shapes to draw
    const numShapes = Math.floor(canvas.width * canvas.height / 40000);
    
    for (let i = 0; i < numShapes; i++) {
        // Random shape type (0: triangle, 1: rectangle, 2: circle)
        const shapeType = Math.floor(Math.random() * 3);
        
        // Random position
        const x = Math.random() * canvas.width;
        const y = Math.random() * canvas.height;
        
        // Random size
        const size = Math.random() * (canvas.width / 10) + 20;
        
        // Random color
        const color = colorMode === 'random' ? getRandomColor() : color2;
        
        // Draw shape
        ctx.fillStyle = color;
        
        switch (shapeType) {
            case 0: // Triangle
                ctx.beginPath();
                ctx.moveTo(x, y);
                ctx.lineTo(x + size, y + size);
                ctx.lineTo(x - size, y + size);
                ctx.closePath();
                ctx.fill();
                break;
            case 1: // Rectangle
                ctx.fillRect(x - size / 2, y - size / 2, size, size);
                break;
            case 2: // Circle
                ctx.beginPath();
                ctx.arc(x, y, size / 2, 0, Math.PI * 2);
                ctx.fill();
                break;
        }
    }
}

// Generate particles wallpaper
function generateParticles(color1, color2, colorMode) {
    // Fill background
    ctx.fillStyle = color1;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Create particles
    const numParticles = Math.floor(canvas.width * canvas.height / 10000);
    particles = [];
    
    for (let i = 0; i < numParticles; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 5 + 1,
            color: colorMode === 'random' ? getRandomColor() : color2,
            vx: Math.random() * 2 - 1,
            vy: Math.random() * 2 - 1
        });
    }
    
    // Draw initial particles
    drawParticles();
    
    // Start animation
    animateParticles();
}

// Draw particles
function drawParticles() {
    particles.forEach(particle => {
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
        ctx.fillStyle = particle.color;
        ctx.fill();
    });
}

// Animate particles
function animateParticles() {
    // Clear canvas
    ctx.fillStyle = color1Input.value;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Update and draw particles
    particles.forEach(particle => {
        // Update position
        particle.x += particle.vx;
        particle.y += particle.vy;
        
        // Bounce off edges
        if (particle.x < 0 || particle.x > canvas.width) {
            particle.vx *= -1;
        }
        if (particle.y < 0 || particle.y > canvas.height) {
            particle.vy *= -1;
        }
        
        // Draw particle
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
        ctx.fillStyle = particle.color;
        ctx.fill();
    });
    
    // Continue animation
    animationFrameId = requestAnimationFrame(animateParticles);
}

// Generate waves wallpaper
function generateWaves(color1, color2, colorMode) {
    // Fill background
    ctx.fillStyle = color1;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Wave parameters
    const numWaves = 5;
    const waveHeight = canvas.height / 20;
    
    for (let i = 0; i < numWaves; i++) {
        ctx.beginPath();
        
        // Wave color
        const waveColor = colorMode === 'random' ? getRandomColor() : color2;
        ctx.strokeStyle = waveColor;
        ctx.lineWidth = canvas.height / (numWaves * 2);
        
        // Wave frequency and phase
        const frequency = (i + 1) / canvas.width * 5;
        const phase = i * Math.PI / 3;
        
        // Draw wave
        for (let x = 0; x < canvas.width; x++) {
            const y = canvas.height / 2 + 
                     Math.sin(x * frequency + phase) * waveHeight * (i + 1);
            
            if (x === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        
        ctx.stroke();
    }
}

// Get random color
function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Save wallpaper to Supabase
async function saveWallpaper() {
    if (!currentUser) {
        // Show auth container if not logged in
        authContainer.style.display = 'flex';
        return;
    }
    
    if (!currentWallpaper) {
        alert('Please generate a wallpaper first');
        return;
    }
    
    try {
        // Prepare wallpaper data
        const wallpaperData = {
            user_id: currentUser.id,
            style: currentWallpaper.style,
            width: currentWallpaper.width,
            height: currentWallpaper.height,
            created_at: new Date().toISOString()
        };
        
        // Add style-specific properties
        if (currentWallpaper.style === 'ai-generated') {
            wallpaperData.prompt = currentWallpaper.prompt;
        } else {
            wallpaperData.color1 = currentWallpaper.color1;
            wallpaperData.color2 = currentWallpaper.color2;
            wallpaperData.color_mode = currentWallpaper.colorMode;
            wallpaperData.opacity = currentWallpaper.opacity;
            wallpaperData.blur = currentWallpaper.blur;
        }
        
        // Save wallpaper metadata to Supabase
        const { data, error } = await supabase
            .from('wallpapers')
            .insert([wallpaperData])
            .select();
            
        if (error) throw error;
        
        // Upload image to storage
        const wallpaperId = data[0].id;
        const fileName = `wallpaper_${wallpaperId}.png`;
        
        // Convert data URL to Blob
        const response = await fetch(currentWallpaper.dataUrl);
        const blob = await response.blob();
        
        const { error: uploadError } = await supabase.storage
            .from('wallpapers')
            .upload(`${currentUser.id}/${fileName}`, blob);
            
        if (uploadError) throw uploadError;
        
        alert('Wallpaper saved successfully!');
        
        // Refresh gallery
        loadGallery();
    } catch (error) {
        console.error('Error saving wallpaper:', error);
        alert('Failed to save wallpaper. Please try again.');
    }
}

// Download wallpaper
function downloadWallpaper() {
    if (!currentWallpaper) {
        alert('Please generate a wallpaper first');
        return;
    }
    
    // Create a temporary link element
    const link = document.createElement('a');
    link.href = currentWallpaper.dataUrl;
    link.download = `wallpaper_${canvas.width}x${canvas.height}.png`;
    
    // Trigger download
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Load user's wallpaper gallery
async function loadGallery() {
    if (!currentUser) return;
    
    try {
        // Fetch user's wallpapers from Supabase
        const { data, error } = await supabase
            .from('wallpapers')
            .select('*')
            .eq('user_id', currentUser.id)
            .order('created_at', { ascending: false });
            
        if (error) throw error;
        
        // Clear gallery
        galleryContainer.innerHTML = '';
        
        if (data.length === 0) {
            galleryContainer.innerHTML = '<p>No saved wallpapers yet.</p>';
            return;
        }
        
        // Display wallpapers
        for (const wallpaper of data) {
            const fileName = `wallpaper_${wallpaper.id}.png`;
            
            // Get image URL
            const { data: urlData } = await supabase.storage
                .from('wallpapers')
                .getPublicUrl(`${currentUser.id}/${fileName}`);
                
            const imageUrl = urlData.publicUrl;
            
            // Create gallery item
            const galleryItem = document.createElement('div');
            galleryItem.className = 'gallery-item';
            
            // Prepare gallery item HTML
            let itemHTML = `
                <img src="${imageUrl}" alt="Wallpaper">
                <div class="gallery-item-info">
                    <h3>${wallpaper.width}x${wallpaper.height}</h3>
                    <p>Style: ${wallpaper.style}</p>`;
                    
            // Add prompt for AI-generated wallpapers
            if (wallpaper.style === 'ai-generated' && wallpaper.prompt) {
                itemHTML += `<p class="prompt-text" title="${wallpaper.prompt}">Prompt: ${wallpaper.prompt.length > 50 ? wallpaper.prompt.substring(0, 50) + '...' : wallpaper.prompt}</p>`;
            }
            
            itemHTML += `
                    <div class="gallery-item-actions">
                        <button class="secondary-btn load-btn" data-id="${wallpaper.id}">Load</button>
                        <button class="secondary-btn delete-btn" data-id="${wallpaper.id}">Delete</button>
                    </div>
                </div>
            `;
            
            galleryItem.innerHTML = itemHTML;
            
            // Add event listeners
            galleryItem.querySelector('.load-btn').addEventListener('click', () => loadWallpaperFromGallery(wallpaper, imageUrl));
            galleryItem.querySelector('.delete-btn').addEventListener('click', () => deleteWallpaper(wallpaper.id));
            
            galleryContainer.appendChild(galleryItem);
        }
    } catch (error) {
        console.error('Error loading gallery:', error);
        galleryContainer.innerHTML = '<p>Failed to load gallery. Please try again.</p>';
    }
}

// Load wallpaper from gallery
function loadWallpaperFromGallery(wallpaper, imageUrl) {
    // Set form values
    resolutionSelect.value = `${wallpaper.width}x${wallpaper.height}`;
    
    if (!resolutionSelect.value) {
        resolutionSelect.value = 'custom';
        customResolution.style.display = 'block';
        widthInput.value = wallpaper.width;
        heightInput.value = wallpaper.height;
    } else {
        customResolution.style.display = 'none';
    }
    
    // Set style and show/hide appropriate controls
    styleSelect.value = wallpaper.style;
    
    if (wallpaper.style === 'ai-generated') {
        // Show AI controls and set prompt
        aiControls.style.display = 'block';
        if (wallpaper.prompt) {
            aiPromptInput.value = wallpaper.prompt;
        }
    } else {
        // Hide AI controls and set standard wallpaper controls
        aiControls.style.display = 'none';
        color1Input.value = wallpaper.color1 || '#3498db';
        color2Input.value = wallpaper.color2 || '#e74c3c';
        colorModeSelect.value = wallpaper.color_mode || 'dual';
        opacityInput.value = wallpaper.opacity || 100;
        opacityValue.textContent = (wallpaper.opacity || 100) + '%';
        blurInput.value = wallpaper.blur || 0;
        blurValue.textContent = (wallpaper.blur || 0) + 'px';
    }
    
    // Set canvas size
    setCanvasSize(resolutionSelect.value === 'custom' ? 'custom' : resolutionSelect.value);
    
    // Load image onto canvas
    const img = new Image();
    img.onload = function() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        
        // Apply blur if needed (for non-AI wallpapers)
        if (wallpaper.style !== 'ai-generated' && wallpaper.blur > 0) {
            canvas.style.filter = `blur(${wallpaper.blur}px)`;
        } else {
            canvas.style.filter = 'none';
        }
        
        // Update current wallpaper data
        if (wallpaper.style === 'ai-generated') {
            currentWallpaper = {
                style: wallpaper.style,
                prompt: wallpaper.prompt,
                width: canvas.width,
                height: canvas.height,
                dataUrl: canvas.toDataURL('image/png')
            };
        } else {
            currentWallpaper = {
                style: wallpaper.style,
                color1: wallpaper.color1,
                color2: wallpaper.color2,
                colorMode: wallpaper.color_mode,
                opacity: wallpaper.opacity,
                blur: wallpaper.blur,
                width: canvas.width,
                height: canvas.height,
                dataUrl: canvas.toDataURL('image/png')
            };
        }
    };
    img.src = imageUrl;
}

// Delete wallpaper
async function deleteWallpaper(id) {
    if (!confirm('Are you sure you want to delete this wallpaper?')) {
        return;
    }
    
    try {
        // Delete wallpaper from database
        const { error } = await supabase
            .from('wallpapers')
            .delete()
            .eq('id', id);
            
        if (error) throw error;
        
        // Delete image from storage
        const fileName = `wallpaper_${id}.png`;
        const { error: storageError } = await supabase.storage
            .from('wallpapers')
            .remove([`${currentUser.id}/${fileName}`]);
            
        if (storageError) throw storageError;
        
        alert('Wallpaper deleted successfully!');
        
        // Refresh gallery
        loadGallery();
    } catch (error) {
        console.error('Error deleting wallpaper:', error);
        alert('Failed to delete wallpaper. Please try again.');
    }
}

// Authentication functions
async function handleSignIn() {
    const email = emailInput.value;
    const password = passwordInput.value;
    
    if (!email || !password) {
        alert('Please enter email and password');
        return;
    }
    
    try {
        const { data, error } = await supabase.auth.signInWithPassword({
            email,
            password
        });
        
        if (error) throw error;
        
        // Hide auth container
        authContainer.style.display = 'none';
        
        // Clear form
        emailInput.value = '';
        passwordInput.value = '';
        
        // Update UI
        currentUser = data.user;
        updateAuthUI();
        
        // Load gallery
        loadGallery();
    } catch (error) {
        console.error('Error signing in:', error);
        alert('Failed to sign in. Please check your credentials and try again.');
    }
}

async function handleSignUp() {
    const email = emailInput.value;
    const password = passwordInput.value;
    
    if (!email || !password) {
        alert('Please enter email and password');
        return;
    }
    
    try {
        const { data, error } = await supabase.auth.signUp({
            email,
            password
        });
        
        if (error) throw error;
        
        alert('Sign up successful! Please check your email for verification.');
        
        // Hide auth container
        authContainer.style.display = 'none';
        
        // Clear form
        emailInput.value = '';
        passwordInput.value = '';
    } catch (error) {
        console.error('Error signing up:', error);
        alert('Failed to sign up. Please try again.');
    }
}

async function checkAuthState() {
    try {
        const { data, error } = await supabase.auth.getSession();
        
        if (error) throw error;
        
        if (data.session) {
            currentUser = data.session.user;
            updateAuthUI();
            loadGallery();
        }
    } catch (error) {
        console.error('Error checking auth state:', error);
    }
}

function updateAuthUI() {
    // Update UI based on authentication state
    if (currentUser) {
        saveBtn.textContent = 'Save to Gallery';
    } else {
        saveBtn.textContent = 'Sign In to Save';
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', init);
