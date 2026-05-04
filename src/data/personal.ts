import type { PersonalInfo } from '../types/types';

/**
 * Personal Information
 * Contains all personal and contact data
 * Used across: Header, Footer, Contact Page, Meta Tags
 */

export const personalInfo: PersonalInfo = {
    id: 'personal-001',
    fullName: 'Abdur Rahman',
    title: 'Data Science Specialist | Developer | Growing Partner',
    tagline: 'Building intelligent systems that turn complex problems into measurable solutions',
    bio: 'Started with web development, learned growth through marketing, now leading with data science. With 4+ years of experience in full-stack development and 2+ years in data science and ML, I bridge the gap between technical excellence and business impact. I specialize in developing intelligent systems, building scalable data pipelines, and creating AI-driven solutions that deliver measurable results.',
    email: 'abdurrahmansoftw@gmail.com',
    phone: '01705952160',
    location: 'Dhaka, Bangladesh',
    timezone: 'GMT+6',
    avatar: '/assets/avatar.jpg',
    coverImage: '/assets/cover.jpg',
    availability: 'Open to Full-time Remote Opportunities, Contract Projects, Consulting',
};

/**
 * Export as singleton for easy access
 */
export default personalInfo;
