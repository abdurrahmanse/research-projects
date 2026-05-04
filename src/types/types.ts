/**
 * TypeScript Types and Interfaces
 * Central location for all data type definitions
 */

// ============================================
// PERSONAL INFORMATION TYPES
// ============================================
export interface PersonalInfo {
    id: string;
    fullName: string;
    title: string;
    tagline: string;
    bio: string;
    email: string;
    phone: string;
    location: string;
    timezone: string;
    avatar?: string;
    coverImage?: string;
    availability: string;
}

// ============================================
// WORK EXPERIENCE TYPES
// ============================================
export interface WorkAchievement {
    id: string;
    metric: string;
    improvement: string;
    description: string;
}

export interface WorkExperience {
    id: string;
    jobTitle: string;
    company: string;
    employmentType: string;
    startDate: string;
    endDate: string | null;
    isCurrent: boolean;
    location: string;
    duration: string;
    description: string;
    responsibilities: string[];
    achievements: WorkAchievement[];
    skills: string[];
    companyLogo?: string;
}

// ============================================
// EDUCATION TYPES
// ============================================
export interface Education {
    id: string;
    degree: string;
    institution: string;
    startDate: string;
    endDate: string;
    status: 'pursuing' | 'completed';
    gpa: string;
    location: string;
    description: string;
    keyCourseworks: string[];
    highlights: string[];
}

// ============================================
// SKILLS TYPES
// ============================================
export interface Skill {
    name: string;
    proficiency: 'Beginner' | 'Intermediate' | 'Advanced' | 'Expert';
    years: number;
    endorsements: number;
    description: string;
}

export interface SkillCategory {
    category: string;
    skills: Skill[];
}

export interface SoftSkill {
    name: string;
    proficiency: 'Intermediate' | 'Advanced' | 'Expert';
    endorsements: number;
    description: string;
}

// ============================================
// ACHIEVEMENT TYPES (Portfolio Awards)
// ============================================
export interface Achievement {
    id: string;
    title: string;
    category: string;
    issuer: string;
    awardDate: string;
    description: string;
    impact: string;
    badge?: string;
    featured?: boolean;
}

// ============================================
// PROJECT TYPES
// ============================================
export interface ProjectImpact {
    [key: string]: string | number | undefined;
    metric?: string;
    improvement?: string;
    efficiency?: string;
    reduction?: string;
    value?: number;
    description?: string;
}

export interface ProjectLinks {
    github?: string;
    demo?: string;
    documentation?: string;
    case_study?: string;
}

export interface Project {
    id: string;
    title: string;
    shortDescription: string;
    fullDescription: string;
    category: string;
    tags: string[];
    startDate: string;
    endDate: string;
    status: 'completed' | 'in-progress' | 'planned';
    featured: boolean;
    images: string[];
    thumbnail: string;
    technologies: string[];
    keyFeatures: string[];
    impact: ProjectImpact;
    links: ProjectLinks;
    relatedPublication?: string;
}

// ============================================
// PUBLICATION TYPES
// ============================================
export interface Publication {
    id: string;
    title: string;
    authors: string[];
    journal: string;
    publishedDate: string;
    volume: string;
    issue: string;
    pages: string;
    doi: string;
    abstract: string;
    keywords: string[];
    type: 'journal' | 'conference' | 'paper';
    status: 'published' | 'submitted';
    links: {
        paper: string;
        doi: string;
        github?: string;
    };
    citations: number;
    downloads: number;
    researchArea: string;
}

// ============================================
// CASE STUDY TYPES
// ============================================
export interface CaseStudyMetric {
    label: string;
    value: string;
    description: string;
}

export interface CaseStudy {
    id: string;
    title: string;
    slug: string;
    company: string;
    industry: string;
    description: string;
    challenge: string;
    solution: string;
    results: Record<string, string | number>;
    technologies: string[];
    keyMetrics: CaseStudyMetric[];
    testimonial: string;
    testimonialAuthor: string;
    image: string;
}

// ============================================
// BLOG TYPES
// ============================================
export interface BlogPost {
    id: string;
    title: string;
    slug: string;
    excerpt: string;
    content: string;
    author: string;
    publishedDate: string;
    updatedDate?: string;
    category: string;
    tags: string[];
    readTime: number;
    image: string;
    featured: boolean;
    views: number;
    likes: number;
    comments: number;
}

// ============================================
// CERTIFICATION TYPES
// ============================================
export interface Certification {
    id: string;
    name: string;
    issuer: string;
    issueDate: string;
    expiryDate?: string;
    credentialId: string;
    credentialUrl: string;
    status: 'active' | 'expired';
    skills: string[];
    description: string;
}

// ============================================
// ACHIEVEMENT TYPES
// ============================================
export interface AchievementRecord {
    id: string;
    title: string;
    award: string;
    awardDate: string;
    category: string;
    description: string;
    icon: string;
}

// ============================================
// TESTIMONIAL TYPES
// ============================================
export interface Testimonial {
    id: string;
    name: string;
    title: string;
    company: string;
    image: string;
    testimonial: string;
    rating: number;
    relationship: 'Manager' | 'Colleague' | 'Mentor' | 'Mentee' | 'Client';
    linkedIn?: string;
    verified?: boolean;
}

// ============================================
// SERVICE TYPES
// ============================================
export interface Service {
    id: string;
    name: string;
    shortDescription: string;
    fullDescription: string;
    category: string;
    icon: string;
    price: string;
    deliverables: string[];
    technologies: string[];
    timeline: string;
    featured?: boolean;
}

// ============================================
// FAQ TYPES
// ============================================
export interface FAQ {
    id: string;
    question: string;
    answer: string;
    category: string;
    priority: number;
}

// ============================================
// SOCIAL LINKS TYPES
// ============================================
export interface SocialLink {
    platform: string;
    url: string;
    icon: string;
    followers?: number;
}

// ============================================
// STATISTICS TYPES
// ============================================
export interface Statistics {
    yearsExperience: number;
    yearsInDataScience: number;
    projectsCompleted: number;
    clientsServed: number;
    linesOfCodeWritten: number;
    publishedPapers: number;
    openSourceContributions: number;
    githubStars: number;
    certifications: number;
    socialFollowers: Record<string, number>;
}
