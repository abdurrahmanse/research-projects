import type { PersonalInfo } from '@/data';
import { personalInfo } from '@/data';

/**
 * Hook for accessing personal information
 * @returns Personal information object with contact details
 */
export const usePersonal = (): PersonalInfo => {
    return personalInfo;
};

/**
 * Hook for getting email address
 * @returns Email address
 */
export const useEmail = (): string => {
    return personalInfo.email;
};

/**
 * Hook for getting phone number
 * @returns Phone number
 */
export const usePhone = (): string => {
    return personalInfo.phone;
};

/**
 * Hook for getting social links from personal info
 * @returns Object with social profile links
 */
export const useContactInfo = () => {
    return {
        email: personalInfo.email,
        phone: personalInfo.phone,
        location: personalInfo.location,
        timezone: personalInfo.timezone,
        availability: personalInfo.availability,
    };
};
