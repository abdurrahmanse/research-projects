/**
 * Social Links & Profiles
 * Contains all social media and external profile links
 * Used on: Homepage (footer/header), About Page, Contact
 */

export interface SocialLink {
    id: string;
    platform: string;
    name: string;
    url: string;
    icon: string;
    followers?: number;
    description?: string;
}

export const socialLinks: SocialLink[] = [
    {
        id: 'social-001',
        platform: 'GitHub',
        name: 'GitHub',
        url: 'https://github.com/abdurrahmanse',
        icon: 'github',
        followers: 1850,
        description: 'Open-source projects and portfolio work',
    },
    {
        id: 'social-002',
        platform: 'LinkedIn',
        name: 'LinkedIn',
        url: 'https://linkedin.com/in/abdur-rahman',
        icon: 'linkedin',
        followers: 3420,
        description: 'Professional profile and career updates',
    },
    {
        id: 'social-003',
        platform: 'Twitter',
        name: 'Twitter/X',
        url: 'https://twitter.com/abdurrahmanse',
        icon: 'twitter',
        followers: 2150,
        description: 'Tech insights and industry discussions',
    },
    {
        id: 'social-004',
        platform: 'Kaggle',
        name: 'Kaggle',
        url: 'https://kaggle.com/abdurrahman',
        icon: 'kaggle',
        followers: 856,
        description: 'Data science competitions and datasets',
    },
    {
        id: 'social-005',
        platform: 'Medium',
        name: 'Medium',
        url: 'https://medium.com/@abdurrahman',
        icon: 'medium',
        description: 'In-depth technical articles and tutorials',
    },
    {
        id: 'social-006',
        platform: 'Email',
        name: 'Email',
        url: 'mailto:abdur@abdurrahmans.dev',
        icon: 'mail',
        description: 'Direct contact',
    },
];

/**
 * Get social link by ID
 */
export const getSocialLinkById = (id: string): SocialLink | undefined => {
    return socialLinks.find((link) => link.id === id);
};

/**
 * Get social link by platform
 */
export const getSocialLinkByPlatform = (platform: string): SocialLink | undefined => {
    return socialLinks.find((link) => link.platform === platform);
};

/**
 * Get all social links
 */
export const getAllSocialLinks = (): SocialLink[] => {
    return socialLinks;
};

/**
 * Get social links with follower counts
 */
export const getSocialLinksWithFollowers = (): SocialLink[] => {
    return socialLinks.filter((link) => link.followers !== undefined && link.followers > 0);
};

/**
 * Get total followers across platforms
 */
export const getTotalFollowers = (): number => {
    return socialLinks.reduce((total, link) => total + (link.followers || 0), 0);
};

/**
 * Get social links sorted by follower count
 */
export const getSocialLinksSortedByFollowers = (): SocialLink[] => {
    return [...socialLinks]
        .filter((link) => link.followers !== undefined)
        .sort((a, b) => (b.followers || 0) - (a.followers || 0));
};

/**
 * Get all platform names
 */
export const getPlatforms = (): string[] => {
    return socialLinks.map((link) => link.platform);
};

export default socialLinks;
