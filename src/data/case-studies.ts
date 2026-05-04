import type { CaseStudy } from '../types/types';

/**
 * Case Studies
 * Contains detailed client success stories
 * Used on: Case Studies Page, Portfolio Section
 */

export const caseStudies: CaseStudy[] = [
    {
        id: 'cs-001',
        title: 'Customer Segmentation at E-commerce Scale',
        slug: 'ecommerce-segmentation',
        company: 'Servier Pharmaceuticals Ltd',
        industry: 'Pharmaceuticals & Healthcare',
        description: 'How we built an ML-powered customer segmentation system that improved targeting accuracy by 35% and campaign ROI by 23%.',
        challenge:
            'The client was using basic demographic segmentation for their marketing campaigns, resulting in poor targeting accuracy and low campaign ROI. With millions of customers and complex behavior patterns, manual segmentation was impossible to scale.',
        solution:
            'We developed a transformer-based ML system that analyzes customer behavior patterns, purchase history, and engagement metrics to create 7 distinct customer segments with actionable insights. The system updates in real-time and integrates with their marketing automation platform.',
        results: {
            targeting_accuracy: '+35%',
            campaign_roi: '+23%',
            customer_retention: '+34%',
            implementation_time: '4 months',
        },
        technologies: ['Python', 'BERT', 'PyTorch', 'PostgreSQL', 'Apache Spark'],
        keyMetrics: [
            {
                label: 'Accuracy Improvement',
                value: '35%',
                description: 'from 62% to 97% segmentation accuracy',
            },
            {
                label: 'ROI Increase',
                value: '23%',
                description: 'in marketing campaign performance',
            },
            {
                label: 'Customer Retention',
                value: '+34%',
                description: 'improved through personalization',
            },
        ],
        testimonial: 'Abdur\'s solution transformed our marketing effectiveness. We now have a data-driven understanding of our customers that was previously impossible to achieve.',
        testimonialAuthor: 'Dr. Ahmed Hassan, CDO',
        image: '/assets/case-studies/segmentation.jpg',
    },
    {
        id: 'cs-002',
        title: 'Healthcare AI Chatbot Implementation',
        slug: 'healthcare-chatbot',
        company: 'Healthcare Innovation Labs',
        industry: 'Healthcare',
        description: 'Building an NLP-powered chatbot that improved patient satisfaction by 45% and reduced administrative overhead by 25%.',
        challenge:
            'The hospital was experiencing long wait times for appointment scheduling and patient inquiries. Their support team was overwhelmed with repetitive queries, and patients were frustrated with limited access to medical information.',
        solution:
            'We built an AI-powered chatbot using BERT and transformer models that understands patient queries in both English and Bengali, provides evidence-based medical information, and seamlessly handles appointment scheduling. The system integrates with their hospital management system and provides 24/7 availability.',
        results: {
            patient_satisfaction: '+45%',
            admin_overhead: '-25%',
            appointment_no_shows: '-30%',
            query_resolution: '92% accuracy',
        },
        technologies: ['Python', 'TensorFlow', 'BERT', 'Flask', 'PostgreSQL', 'AWS'],
        keyMetrics: [
            {
                label: 'Patient Satisfaction',
                value: '+45%',
                description: 'significant improvement in satisfaction scores',
            },
            {
                label: 'Administrative Efficiency',
                value: '-25%',
                description: 'reduction in overhead costs',
            },
            {
                label: 'Query Resolution Accuracy',
                value: '92%',
                description: 'correct response to patient queries',
            },
        ],
        testimonial: 'This chatbot has been transformative for our operations. Our staff can now focus on more complex cases while patients get immediate responses to their questions.',
        testimonialAuthor: 'Dr. James Wilson, CTO',
        image: '/assets/case-studies/healthcare-chatbot.jpg',
    },
    {
        id: 'cs-003',
        title: 'E-commerce Performance Optimization',
        slug: 'ecommerce-optimization',
        company: 'Leading E-commerce Platform',
        industry: 'E-commerce',
        description: 'Achieving 50% performance improvement resulting in 28% increase in conversion rate and significant revenue growth.',
        challenge:
            'The e-commerce platform had a page load time of 5+ seconds, causing high bounce rates and lost conversions. The site wasn\'t optimized for mobile, and SEO performance was suffering due to poor Core Web Vitals.',
        solution:
            'We implemented comprehensive optimization: code splitting, lazy loading, server-side rendering, database optimization, and CDN integration. We also improved image optimization and implemented a robust caching strategy.',
        results: {
            page_load_time: '-50%',
            conversion_rate: '+28%',
            bounce_rate: '-35%',
            revenue_impact: '+€2.5M annually',
        },
        technologies: ['Next.js', 'React', 'TypeScript', 'Node.js', 'Redis', 'CloudFront'],
        keyMetrics: [
            {
                label: 'Page Load Time',
                value: '2.5s',
                description: 'from 5+ seconds',
            },
            {
                label: 'Conversion Rate',
                value: '+28%',
                description: 'direct improvement from optimization',
            },
            {
                label: 'Annual Revenue Impact',
                value: '€2.5M',
                description: 'additional revenue from improved UX',
            },
        ],
        testimonial: 'The performance improvement directly translated to significant revenue growth. This was one of the best investments we made.',
        testimonialAuthor: 'Maria Rodriguez, Product Manager',
        image: '/assets/case-studies/ecommerce.jpg',
    },
];

/**
 * Get case study by ID
 */
export const getCaseStudyById = (id: string): CaseStudy | undefined => {
    return caseStudies.find((cs) => cs.id === id);
};

/**
 * Get case study by slug
 */
export const getCaseStudyBySlug = (slug: string): CaseStudy | undefined => {
    return caseStudies.find((cs) => cs.slug === slug);
};

/**
 * Get case studies by industry
 */
export const getCaseStudiesByIndustry = (industry: string): CaseStudy[] => {
    return caseStudies.filter((cs) => cs.industry === industry);
};

/**
 * Get case studies by company
 */
export const getCaseStudiesByCompany = (company: string): CaseStudy[] => {
    return caseStudies.filter((cs) => cs.company === company);
};

/**
 * Get all industries
 */
export const getIndustries = (): string[] => {
    const industries = new Set<string>();
    caseStudies.forEach((cs) => {
        industries.add(cs.industry);
    });
    return Array.from(industries);
};

/**
 * Get all companies
 */
export const getCompanies = (): string[] => {
    return caseStudies.map((cs) => cs.company);
};

export default caseStudies;
