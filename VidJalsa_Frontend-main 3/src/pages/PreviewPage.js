import React, { useEffect, useRef, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import styles from '../css/preview.module.css'; 

const PreviewPage = () => {
    const navigate = useNavigate();

    const location = useLocation();
    const videosInfo = location.state?.videosInfo;
    const topic = location.state?.topic;
    const containerRef = useRef(null);
    const [centerIndex, setCenterIndex] = useState(null);
    const [isFirstItemCentered, setIsFirstItemCentered] = useState(true);
    const [isLastItemCentered, setIsLastItemCentered] = useState(false);
    const [selectedVideos, setSelectedVideos] = useState([]);
    const [showSelectionInfo, setShowSelectionInfo] = useState(false);

    useEffect(() => {
        setShowSelectionInfo(selectedVideos.length > 0);
      }, [selectedVideos]);      

    const scrollToNext = () => {
        const container = containerRef.current;
        if (!container || centerIndex === null || videosInfo.length === 0) return;

        let nextIndex = centerIndex + 1;
        if (nextIndex >= videosInfo.length) return;

        const nextItem = container.children[nextIndex];
        if (nextItem) {
            const topPos = nextItem.offsetTop - (container.offsetHeight / 2) + (nextItem.offsetHeight / 2);
            container.scrollTo({ top: topPos, behavior: 'smooth' });
        }
    };

    const scrollToPrev = () => {
        const container = containerRef.current;
        if (!container || centerIndex === null || videosInfo.length === 0) return;

        if (centerIndex === 0) {
            container.scrollTo({ top: 0, behavior: 'smooth' });
            return;
        }

        let targetIndex = centerIndex - 1;
        targetIndex = Math.max(targetIndex, 0);

        const targetItem = container.children[targetIndex];
        if (targetItem) {
            const topPos = targetItem.offsetTop - (container.offsetHeight / 2) + (targetItem.offsetHeight / 2);
            container.scrollTo({ top: topPos, behavior: 'smooth' });
        }
    };

    useEffect(() => {
        const calculateCenterIndex = () => {
            const container = containerRef.current;
            const scrollTop = container.scrollTop;
            const containerHeight = container.offsetHeight;
            let closestIndex = null;
            let closestDistance = null;
            const children = container.children; 

            for (let i = 0; i < children.length; i++) {
                const child = children[i];
                const childTop = child.offsetTop - container.offsetTop;
                const childHeight = child.offsetHeight;
                const childCenter = childTop + childHeight / 2;
                const containerCenter = scrollTop + containerHeight / 2;
                const distance = Math.abs(containerCenter - childCenter);

                if (closestDistance === null || distance < closestDistance) {
                    closestDistance = distance;
                    closestIndex = i;
                }
            }
            setCenterIndex(closestIndex);

            setIsFirstItemCentered(closestIndex === 0);
            setIsLastItemCentered(closestIndex === videosInfo.length - 1);
        };

        const container = containerRef.current;
        container.addEventListener('scroll', calculateCenterIndex);
        calculateCenterIndex(); 

        return () => container.removeEventListener('scroll', calculateCenterIndex);
    }, [videosInfo]);

    const handleCheckboxChange = (video) => {
        setSelectedVideos(prev => {
            if (prev.find(item => item.link === video.link)) {
                return prev.filter(l => l.link !== video.link);
            } else {
                if (prev.length >= 5) {
                    return prev;
                }
                return [...prev, video];
            }
        });
    };

    function decodeHtml(html) {
        var txt = document.createElement('textarea');
        txt.innerHTML = html;
        return txt.value;
    }
        
    const handleSubmit = () => {
        const videoLinks = selectedVideos.map(video => video.link);
        navigate('/loading', { state: { videoLinks: videoLinks, topic: topic, videoInfo: selectedVideos } });
    };
    
        
    return (
        <div className={styles.previewContainer}>
            <div className={styles.fadeContainer}> 
                {<button className={`${styles.scrollButton} ${!isFirstItemCentered ? styles.visible : ''}`} onClick={scrollToPrev}>&#9650;</button>}
                <div className={styles.topFade}></div> 
                <div className={styles.leftContainer} ref={containerRef}>
                {videosInfo && videosInfo.map((video, index) => (
                    <div key={index} className={`${styles.videoContainer} ${index === centerIndex ? styles.centered : ''}`}>
                        <div className={styles.videoContent}>
                            <div className={styles.videoThumbnailContainer}>
                                <a href={video.link} target="_blank" rel="noopener noreferrer" className={styles.videoLink}>
                                    <img src={video.thumbnail} alt={video.title} className={styles.videoThumbnail} />
                                    <div className={styles.videoDuration}>{Math.floor((video.duration - 1) / 60)}:{String((video.duration - 1) % 60).padStart(2, '0')}</div>
                                </a>
                            </div>
                            <div className={`${styles.checkboxContainer} ${index === centerIndex ? styles.visible : ''}`}>
                            <input 
                                type="checkbox" 
                                className={styles.checkbox} 
                                checked={selectedVideos.some(item => item.link === video.link)}
                                onChange={() => handleCheckboxChange(video)} 
                            />
                            </div>
                        </div>
                        <p className={`${styles.videoTitle} ${index === centerIndex ? styles.visible : ''}`}>{decodeHtml(video.title)}</p>
                    </div>
                ))}

                </div>
                <div className={styles.bottomFade}></div> 
                {<button className={`${styles.scrollButton} ${!isLastItemCentered ? styles.visible : ''}`} onClick={scrollToNext}>&#9660;</button>}
            </div>
            <div className={styles.rightContainer}>
                <h1 className={styles.gradientText} style={{fontFamily: 'Yeseva One'}}>Preview Your Videos</h1>
                <h1 className={styles.gradientText} style={{fontSize: '3rem'}}>Pick A Min. Of 1 And A Max. Of 5</h1>
                <div className={`${styles.selectionInfo} ${showSelectionInfo ? styles.show : ''}`}>
                    <span className={styles.videoCount} style={{fontWeight:'Bold'}}># Of Videos: {selectedVideos.length}</span>
                    <button 
                        type="submit"
                        className={styles.submitArrowButton}
                        aria-label="Submit"
                        onClick={handleSubmit}
                    >
                        <span className={styles.buttonText} style={{fontWeight:'bold'}}>Create</span>
                        <img src={require('../assets/stars.png')} alt="Stars" style={{width:'35px', marginLeft:'5px', marginRight:'-10px'}} />
                    </button>
                </div>
            </div>

        </div>
    );
};

export default PreviewPage;
