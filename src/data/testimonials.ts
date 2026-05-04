import type { Testimonial } from '../types/types';

/**
 * Testimonials
 * Contains client and colleague testimonials
 * Used on: Homepage, Testimonials Page, About Page
 */

export const testimonials: Testimonial[] = [
    {
        id: 'testimonial-001',
        name: 'Dr. Ahmed Hassan',
        title: 'Chief Data Officer',
        company: 'Servier Pharmaceuticals Ltd',
        image: '/assets/testimonials/ahmed-hassan.jpg',
        testimonial:
            'Abdur\'s work on our customer segmentation project was exceptional. He not only delivered a solution that improved our targeting accuracy by 35% but also took the time to ensure our team understood the ML concepts behind it. His communication skills are outstanding.',
        rating: 5,
        relationship: 'Client',
        linkedIn: 'https://linkedin.com/in/ahmed-hassan',
        verified: true,
    },
    {
        id: 'testimonial-002',
        name: 'Dr. James Wilson',
        title: 'Chief Technology Officer',
        company: 'Healthcare Innovation Labs',
        image: '/assets/testimonials/james-wilson.jpg',
        testimonial:
            'The healthcare chatbot Abdur built transformed our patient engagement strategy. It\'s robust, intelligent, and has genuinely improved our patient satisfaction scores. Working with him was a pleasure - very professional and results-oriented.',
        rating: 5,
        relationship: 'Client',
        linkedIn: 'https://linkedin.com/in/james-wilson',
        verified: true,
    },
    {
        id: 'testimonial-003',
        name: 'Maria Rodriguez',
        title: 'Product Manager',
        company: 'Leading E-commerce Platform',
        image: '/assets/testimonials/maria-rodriguez.jpg',
        testimonial:
            'Abdur\'s optimization work resulted in a 50% performance improvement that directly impacted our bottom line. His technical expertise combined with his business acumen is rare. Highly recommend for any serious performance challenge.',
        rating: 5,
        relationship: 'Client',
        linkedIn: 'https://linkedin.com/in/maria-rodriguez',
        verified: true,
    },
    {
        id: 'testimonial-004',
        name: 'Prof. Sarah Chen',
        title: 'Professor of Computer Science',
        company: 'University of Technology',
        image: '/assets/testimonials/sarah-chen.jpg',
        testimonial:
            'Abdur is an exceptional researcher and practitioner in machine learning. His publications are insightful, and his ability to translate academic concepts into practical solutions is impressive. He\'d be an asset to any organization.',
        rating: 5,
        relationship: 'Mentor',
        linkedIn: 'https://linkedin.com/in/sarah-chen',
        verified: true,
    },
    {
        id: 'testimonial-005',
        name: 'Michael Thompson',
        title: 'Senior Developer',
        company: 'Tech Startup Inc',
        image: '/assets/testimonials/michael-thompson.jpg',
        testimonial:
            'I had the pleasure of working with Abdur on several projects. His code is clean, well-documented, and production-ready. More importantly, he\'s a great team player who mentors junior developers effectively. One of the best developers I\'ve worked with.',
        rating: 5,
        relationship: 'Colleague',
        linkedIn: 'https://linkedin.com/in/michael-thompson',
        verified: true,
    },
];

/**
 * Get testimonial by ID
 */
export const getTestimonialById = (id: string): Testimonial | undefined => {
    return testimonials.find((testimonial) => testimonial.id === id);
};

/**
 * Get testimonials by rating
 */
export const getTestimonialsByRating = (rating: number): Testimonial[] => {
    return testimonials.filter((testimonial) => testimonial.rating === rating);
};

/**
 * Get testimonials by relationship
 */
export const getTestimonialsByRelationship = (relationship: string): Testimonial[] => {
    return testimonials.filter((testimonial) => testimonial.relationship === relationship);
};

/**
 * Get verified testimonials only
 */
export const getVerifiedTestimonials = (): Testimonial[] => {
    return testimonials.filter((testimonial) => testimonial.verified);
};

/**
 * Get testimonials by company
 */
export const getTestimonialsByCompany = (company: string): Testimonial[] => {
    return testimonials.filter((testimonial) => testimonial.company === company);
};

/**
 * Get all unique companies
 */
export const getCompanies = (): string[] => {
    const companies = new Set<string>();
    testimonials.forEach((testimonial) => {
        companies.add(testimonial.company);
    });
    return Array.from(companies);
};

/**
 * Get all unique relationships
 */
export const getRelationships = (): string[] => {
    const relationships = new Set<string>();
    testimonials.forEach((testimonial) => {
        relationships.add(testimonial.relationship);
    });
    return Array.from(relationships);
};

/**
 * Get average rating
 */
export const getAverageRating = (): number => {
    const totalRating = testimonials.reduce((sum, testimonial) => sum + testimonial.rating, 0);
    return totalRating / testimonials.length;
};

/**
 * Get testimonial count by rating
 */
export const getTestimonialCountByRating = (): Record<number, number> => {
    const ratingCounts: Record<number, number> = {};
    testimonials.forEach((testimonial) => {
        ratingCounts[testimonial.rating] = (ratingCounts[testimonial.rating] || 0) + 1;
    });
    return ratingCounts;
};

export default testimonials;
