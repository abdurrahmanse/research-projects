import type { SocialLink } from '@/data';
import {
    getAllSocialLinks,
    getPlatforms,
    getSocialLinkById,
    getSocialLinkByPlatform,
    getSocialLinksSortedByFollowers,
    getSocialLinksWithFollowers,
    getTotalFollowers,
    socialLinks,
} from '@/data';

/**
 * Hook for accessing all social links
 * @returns Array of all social links
 */
export const useSocialLinks = (): SocialLink[] => {
    return getAllSocialLinks();
};

/**
 * Hook for getting social link by ID
 * @param id - Social link ID
 * @returns Social link or undefined
 */
export const useSocialLinkById = (id: string): SocialLink | undefined => {
    return getSocialLinkById(id);
};

/**
 * Hook for getting social link by platform
 * @param platform - Platform name
 * @returns Social link or undefined
 */
export const useSocialLinkByPlatform = (platform: string): SocialLink | undefined => {
    return getSocialLinkByPlatform(platform);
};

/**
 * Hook for getting social links with follower counts
 * @returns Array of social links with followers
 */
export const useSocialLinksWithFollowers = (): SocialLink[] => {
    return getSocialLinksWithFollowers();
};

/**
 * Hook for getting total followers across all platforms
 * @returns Total follower count
 */
export const useTotalFollowers = (): number => {
    return getTotalFollowers();
};

/**
 * Hook for getting social links sorted by follower count (highest first)
 * @returns Array of social links sorted by followers
 */
export const useSocialLinksSortedByFollowers = (): SocialLink[] => {
    return getSocialLinksSortedByFollowers();
};

/**
 * Hook for getting all platform names
 * @returns Array of platform names
 */
export const useSocialPlatforms = (): string[] => {
    return getPlatforms();
};

/**
 * Hook for getting social link count
 * @returns Total number of social links
 */
export const useSocialLinkCount = (): number => {
    return socialLinks.length;
};

/**
 * Hook for getting most followed platform
 * @returns Platform with most followers or undefined
 */
export const useMostFollowedPlatform = (): SocialLink | undefined => {
    return getSocialLinksSortedByFollowers()[0];
};

/**
 * Hook for getting average followers per platform
 * @returns Average follower count
 */
export const useAverageFollowersPerPlatform = (): number => {
    const linksWithFollowers = getSocialLinksWithFollowers();
    return linksWithFollowers.length > 0
        ? getTotalFollowers() / linksWithFollowers.length
        : 0;
};
