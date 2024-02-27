import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import styles from '../css/loading.module.css';
import MeteorShowers from '../components/MeteorShowers';
import ProgressBar from "@ramonak/react-progress-bar";

function LoadingPage() {
    const [loadingPercentage, setLoadingPercentage] = useState(0);
    const location = useLocation();
    const navigate = useNavigate();
    const processingFinished = useRef(false);
    const deploymentUrlRef = useRef('');

    useEffect(() => {
        const startProcessing = async () => {
            const { videoLinks, videoInfo, topic } = location.state;

            try {
                const response = await fetch('http://127.0.0.1:7000/api/v1/process_videos', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ urls: videoLinks, topic: topic }),
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                processingFinished.current = true;
                deploymentUrlRef.current = data.deployment_url;

                // Set to 100% after processing is done
                setLoadingPercentage(100);
            } catch (error) {
                console.error('There was a problem with the fetch operation:', error);
            }
        };

        // Simulate loading over 110 seconds to reach 90%
        const interval = setInterval(() => {
            setLoadingPercentage(prev => {
                if (prev < 90) {
                    return prev + (90 / 110); // Adjust this to control the speed more precisely
                } else if (prev >= 90 && processingFinished.current) {
                    clearInterval(interval); // Stop the interval if processing is finished
                    return 100; // Jump to 100% after processing is done
                }
                return prev; // Keep the current percentage if none of the above conditions are met
            });
        }, 1000); // Run every second

        startProcessing();

        return () => {
            clearInterval(interval); // Cleanup on unmount
        };
    }, []); // Mimics componentDidMount with an empty dependency array

    useEffect(() => {
        if (loadingPercentage === 100) {
            // Wait 2 seconds to show the full animation before navigating
            setTimeout(() => {
                navigate('/output', {
                    state: {
                        videosInfo: location.state.videoInfo,
                        deploymentUrl: deploymentUrlRef.current
                    }
                });
            }, 2000);
        }
    }, [loadingPercentage, navigate, location.state]);

    return (
        <div className={styles.mainContainer}>
            <MeteorShowers loadingPercentage={loadingPercentage} />
            <div className={styles.loadingContainer}>
                <h1 className={styles.gradientText} style={{ fontFamily: 'Yeseva One' }}>Creating Your Blog</h1>
                <h1 className={styles.gradientText} style={{ fontSize: '3rem', marginBottom: '20px' }}>This Might Take A While...</h1>
                <ProgressBar completed={loadingPercentage} bgColor='white' baseBgColor='black' width='600px' height='20px' borderRadius='12px' className='myProgressBar'/>
            </div>
        </div>
    );
}

export default LoadingPage;
