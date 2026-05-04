import type { Certification } from '@/data';
import {
    certifications,
    getActiveCertifications,
    getAllCertificationSkills,
    getCertificationById,
    getCertificationByName,
    getCertificationIssuers,
    getCertificationsByIssuer,
    getCertificationsBySkill,
    getCertificationsExpiringSoon,
    getExpiredCertifications,
} from '@/data';

/**
 * Hook for accessing all certifications
 * @returns Array of all certifications
 */
export const useCertifications = (): Certification[] => {
    return certifications;
};

/**
 * Hook for getting certification by ID
 * @param id - Certification ID
 * @returns Certification or undefined
 */
export const useCertificationById = (id: string): Certification | undefined => {
    return getCertificationById(id);
};

/**
 * Hook for getting certification by name
 * @param name - Certification name
 * @returns Certification or undefined
 */
export const useCertificationByName = (name: string): Certification | undefined => {
    return getCertificationByName(name);
};

/**
 * Hook for getting certifications by issuer
 * @param issuer - Issuer name
 * @returns Array of certifications from issuer
 */
export const useCertificationsByIssuer = (issuer: string): Certification[] => {
    return getCertificationsByIssuer(issuer);
};

/**
 * Hook for getting active certifications only
 * @returns Array of active certifications
 */
export const useActiveCertifications = (): Certification[] => {
    return getActiveCertifications();
};

/**
 * Hook for getting expired certifications
 * @returns Array of expired certifications
 */
export const useExpiredCertifications = (): Certification[] => {
    return getExpiredCertifications();
};

/**
 * Hook for getting certifications expiring soon (within 6 months)
 * @returns Array of certifications expiring soon
 */
export const useCertificationsExpiringSoon = (): Certification[] => {
    return getCertificationsExpiringSoon();
};

/**
 * Hook for getting all certification issuers
 * @returns Array of unique issuer names
 */
export const useCertificationIssuers = (): string[] => {
    return getCertificationIssuers();
};

/**
 * Hook for getting all skills from certifications
 * @returns Array of unique skills
 */
export const useCertificationSkills = (): string[] => {
    return getAllCertificationSkills();
};

/**
 * Hook for filtering certifications by skill
 * @param skill - Skill name
 * @returns Array of certifications covering skill
 */
export const useCertificationsBySkill = (skill: string): Certification[] => {
    return getCertificationsBySkill(skill);
};

/**
 * Hook for getting active certification count
 * @returns Number of active certifications
 */
export const useActiveCertificationCount = (): number => {
    return getActiveCertifications().length;
};

/**
 * Hook for getting total certification count
 * @returns Total number of certifications
 */
export const useCertificationCount = (): number => {
    return certifications.length;
};
