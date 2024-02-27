import React, { useEffect, useRef } from 'react';
import styles from '../css/meteors.module.css';

function MeteorShowers({ loadingPercentage }) {
    const canvasRef = useRef(null);
    const requestRef = useRef();
    const lastUpdateTimeRef = useRef(Date.now());
    const meteors = useRef([]);

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        const scale = window.devicePixelRatio; // Get the device's pixel ratio
        canvas.width = window.innerWidth * scale; // Scale canvas width
        canvas.height = window.innerHeight * scale; // Scale canvas height
        canvas.style.width = window.innerWidth + 'px'; // Set display size
        canvas.style.height = window.innerHeight + 'px'; // Set display size
        ctx.scale(scale, scale); 
    
        const createMeteor = () => {
            const side = Math.random() < 0.5; // Randomly choose if the meteor starts from the top or left
            let x, y;
            if (side) {
                // Start from top
                x = Math.random() * canvas.width;
                y = 0;
            } else {
                // Start from left
                x = 0;
                y = Math.random() * canvas.height;
            }
            const length = Math.random() * (80 - 10) + 30; // Meteor length between 30 and 80
            // Use angles to create more varied directions
            const angle = Math.PI / 4; 
            const speed = Math.random() * (10 - 1) + 5; // Speed between 5 and 10
    
            meteors.current.push({ x, y, length, speed, angle });
        };
    
        const drawMeteors = (time) => {
            const currentTime = Date.now();
            const deltaTime = currentTime - lastUpdateTimeRef.current;
            lastUpdateTimeRef.current = currentTime;
        
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        
            meteors.current.forEach((meteor, index) => {
                // Calculate the new position based on the angle and speed
                const newX = meteor.x + Math.cos(meteor.angle) * meteor.speed;
                const newY = meteor.y + Math.sin(meteor.angle) * meteor.speed;
        
                // Extend the length of the trail by adjusting the starting point further back from the new position
                const tailX = newX - Math.cos(meteor.angle) * meteor.length; // Adjust this to extend the trail
                const tailY = newY - Math.sin(meteor.angle) * meteor.length; // Adjust this to extend the trail
        
                // Create a gradient from the end of the trail (more transparent) to the start (more opaque, where the ball is)
                const gradient = ctx.createLinearGradient(tailX, tailY, newX, newY);
                gradient.addColorStop(0, 'rgba(255,255,255,0)'); // Tail end: more transparent
                gradient.addColorStop(1, 'rgba(255,255,255,0.3)'); // Near the ball: more opaque
        
                // Draw the trail with the gradient
                ctx.beginPath();
                ctx.moveTo(tailX, tailY);
                ctx.lineTo(newX, newY);
                ctx.strokeStyle = gradient;
                ctx.lineWidth = 2; // Thickness of the trail
                ctx.stroke();
        
                // Draw the glowing ball at the new position (the meteor's head)
                ctx.beginPath();
                ctx.arc(newX, newY, 3, 0, 2 * Math.PI, false);
                ctx.fillStyle = 'white';
                ctx.shadowBlur = 10;
                ctx.shadowColor = 'white';
                ctx.fill();
                // Reset shadow to avoid affecting other elements
                ctx.shadowBlur = 0;
        
                // Update the meteor's position for the next frame
                meteor.x = newX;
                meteor.y = newY;
        
                // Remove meteors that move off screen
                if (newX > canvas.width || newY > canvas.height) {
                    meteors.current.splice(index, 1);
                }
            });

            meteors.current = meteors.current.filter(meteor => meteor.x <= canvas.width && meteor.y <= canvas.height);
        
            if (Math.random() < (loadingPercentage / 100) * (deltaTime / 50)) {
                createMeteor();
            }
        
            requestRef.current = requestAnimationFrame(drawMeteors);
        };                       
    
        requestRef.current = requestAnimationFrame(drawMeteors);
    
        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
        window.addEventListener('resize', resize);
    
        return () => {
            window.removeEventListener('resize', resize);
            cancelAnimationFrame(requestRef.current);
        };
    }, [loadingPercentage]);
    

    return <canvas ref={canvasRef} className={styles.canvas}></canvas>;
}

export default MeteorShowers;