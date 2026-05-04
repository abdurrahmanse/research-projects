import type { Certification } from '../types/types';

/**
 * Certifications
 * Contains all professional certifications and credentials
 * Used on: Certifications Page, Resume, LinkedIn
 */

export const certifications: Certification[] = [
    {
        id: 'cert-001',
        name: 'AWS Certified Machine Learning – Specialty',
        issuer: 'Amazon Web Services',
        issueDate: '2024-05-12',
        expiryDate: '2027-05-12',
        credentialId: 'AWS-ML-2024-001',
        credentialUrl: 'https://www.credly.com/badges/aws-ml-specialty',
        status: 'active',
        skills: ['AWS SageMaker', 'Machine Learning', 'Data Analysis', 'Model Deployment'],
        description: 'Validates expertise in building, training, tuning, and deploying ML models on AWS.',
    },
    {
        id: 'cert-002',
        name: 'Google Cloud Professional Data Engineer',
        issuer: 'Google Cloud',
        issueDate: '2024-02-15',
        expiryDate: '2026-02-15',
        credentialId: 'GCP-DE-2024-002',
        credentialUrl: 'https://www.credential.net/gcp-data-engineer',
        status: 'active',
        skills: ['Google Cloud Platform', 'BigQuery', 'Data Engineering', 'Apache Beam'],
        description: 'Demonstrates ability to design and manage data infrastructure on Google Cloud Platform.',
    },
    {
        id: 'cert-003',
        name: 'TensorFlow Certified Developer',
        issuer: 'TensorFlow / Google',
        issueDate: '2023-11-22',
        expiryDate: '2025-11-22',
        credentialId: 'TF-DEV-2023-003',
        credentialUrl: 'https://www.tensorflow.org/certificate',
        status: 'active',
        skills: ['TensorFlow', 'Deep Learning', 'Neural Networks', 'Python'],
        description: 'Certifies proficiency in building ML models using TensorFlow.',
    },
    {
        id: 'cert-004',
        name: 'Certified Kubernetes Application Developer (CKAD)',
        issuer: 'Linux Foundation / CNCF',
        issueDate: '2024-01-10',
        expiryDate: '2027-01-10',
        credentialId: 'CKAD-2024-004',
        credentialUrl: 'https://www.cncf.io/certification/ckad/',
        status: 'active',
        skills: ['Kubernetes', 'DevOps', 'Container Orchestration', 'Docker'],
        description: 'Validates expertise in designing, building, and deploying applications on Kubernetes.',
    },
    {
        id: 'cert-005',
        name: 'Docker Certified Associate',
        issuer: 'Docker',
        issueDate: '2023-08-05',
        expiryDate: '2025-08-05',
        credentialId: 'DCA-2023-005',
        credentialUrl: 'https://www.docker.com/certifications',
        status: 'active',
        skills: ['Docker', 'Containerization', 'Image Management', 'Container Security'],
        description: 'Demonstrates proficiency in designing and implementing containerized applications.',
    },
];

/**
 * Get certification by ID
 */
export const getCertificationById = (id: string): Certification | undefined => {
    return certifications.find((cert) => cert.id === id);
};

/**
 * Get certification by name
 */
export const getCertificationByName = (name: string): Certification | undefined => {
    return certifications.find((cert) => cert.name === name);
};

/**
 * Get certifications by issuer
 */
export const getCertificationsByIssuer = (issuer: string): Certification[] => {
    return certifications.filter((cert) => cert.issuer === issuer);
};

/**
 * Get all active certifications
 */
export const getActiveCertifications = (): Certification[] => {
    const now = new Date();
    return certifications.filter((cert) => cert.status === 'active' && cert.expiryDate && new Date(cert.expiryDate) > now);
};

/**
 * Get expired certifications
 */
export const getExpiredCertifications = (): Certification[] => {
    const now = new Date();
    return certifications.filter((cert) => cert.expiryDate && new Date(cert.expiryDate) <= now);
};

/**
 * Get certifications expiring soon (within 6 months)
 */
export const getCertificationsExpiringSoon = (): Certification[] => {
    const now = new Date();
    const sixMonthsFromNow = new Date(now.getTime() + 6 * 30 * 24 * 60 * 60 * 1000);
    return certifications.filter(
        (cert) => cert.expiryDate && new Date(cert.expiryDate) > now && new Date(cert.expiryDate) <= sixMonthsFromNow,
    );
};

/**
 * Get all unique issuers
 */
export const getIssuers = (): string[] => {
    const issuers = new Set<string>();
    certifications.forEach((cert) => {
        issuers.add(cert.issuer);
    });
    return Array.from(issuers);
};

/**
 * Get all skills from certifications
 */
export const getAllCertificationSkills = (): string[] => {
    const skills = new Set<string>();
    certifications.forEach((cert) => {
        cert.skills.forEach((skill) => {
            skills.add(skill);
        });
    });
    return Array.from(skills);
};

/**
 * Get certifications by skill
 */
export const getCertificationsBySkill = (skill: string): Certification[] => {
    return certifications.filter((cert) => cert.skills.includes(skill));
};

export default certifications;
