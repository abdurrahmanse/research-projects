/**
 * Data Hooks
 * Custom React hooks for accessing portfolio data
 */

// Personal Information
export { useContactInfo, useEmail, usePersonal, usePhone } from './usePersonal';

// Experience & Education
export { useCompanies, useCurrentWork, useExperience, useTotalExperience, useWorkExperienceById } from './useExperience';

export {
    useAllCourseworks, useCompletedEducation, useEducation, useEducationById, useHighestDegree, useOngoingEducation
} from './useEducation';

// Skills
export {
    useAllTechnicalSkillNames, useExpertSkills, useSkillCategories, useSkillsByCategory, useSkillsByProficiency, useSoftSkills, useTechnicalSkills, useTotalEndorsements
} from './useSkills';

// Projects & Work
export {
    useFeaturedProjectCount, useFeaturedProjects,
    useProjectById, useProjectCategories, useProjectCount, useProjects, useProjectsByCategory,
    useProjectsByTechnology, useProjectTechnologies
} from './useProjects';

// Publications
export {
    useAverageCitationsPerPublication, useMostCitedPublication,
    useMostDownloadedPublication, usePublicationById, usePublicationCount, usePublicationKeywords, usePublications, usePublicationsByAuthor,
    usePublicationsByResearchArea, useResearchAreas, useTotalCitations,
    useTotalDownloads
} from './usePublications';

// Blog
export {
    useAverageBlogReadTime, useBlogCategories, useBlogPostById,
    useBlogPostBySlug, useBlogPostCount, useBlogPosts, useBlogPostsByCategory,
    useBlogPostsByTag,
    useBlogPostsSortedByDate,
    useBlogPostsSortedByViews, useBlogTags, useFeaturedBlogPosts, useMostViewedBlogPost,
    useSearchBlogPosts, useTotalBlogViews
} from './useBlog';

// Case Studies
export {
    useCaseStudies, useCaseStudiesByCompany, useCaseStudiesByIndustry, useCaseStudyById,
    useCaseStudyBySlug, useCaseStudyCompanies,
    useCaseStudyCount, useCaseStudyIndustries
} from './useCaseStudies';

// Certifications
export {
    useActiveCertificationCount, useActiveCertifications, useCertificationById,
    useCertificationByName, useCertificationCount, useCertificationIssuers, useCertifications, useCertificationsByIssuer, useCertificationsBySkill, useCertificationsExpiringSoon, useCertificationSkills, useExpiredCertifications
} from './useCertifications';

// Achievements
export {
    useAchievementById, useAchievementCategories, useAchievementCount, useAchievementCountByYear, useAchievementIssuers, useAchievements, useAchievementsByCategory,
    useAchievementsByIssuer,
    useAchievementsSortedByDate, useFeaturedAchievementCount, useFeaturedAchievements
} from './useAchievements';

// Testimonials
export {
    useAllFiveStarTestimonials, useAverageTestimonialRating, useTestimonialById, useTestimonialCompanies, useTestimonialCount, useTestimonialCountByRating, useTestimonialRelationships, useTestimonials, useTestimonialsByCompany, useTestimonialsByRating,
    useTestimonialsByRelationship, useVerifiedTestimonialCount, useVerifiedTestimonials
} from './useTestimonials';

// Services
export {
    useFeaturedServiceCount, useFeaturedServices,
    useServiceById, useServiceCategories, useServiceCount, useServices, useServicesByCategory,
    useServicesByTechnology, useServiceTechnologies
} from './useServices';

// FAQs
export {
    useFAQById, useFAQCategories, useFAQCount, useFAQCountByCategory, useFAQs, useFAQsByCategory,
    useFAQsSortedByPriority, useMostCommonFAQCategory, useSearchFAQs
} from './useFAQs';

// Social Links
export {
    useAverageFollowersPerPlatform, useMostFollowedPlatform, useSocialLinkById,
    useSocialLinkByPlatform, useSocialLinkCount, useSocialLinks, useSocialLinksSortedByFollowers, useSocialLinksWithFollowers, useSocialPlatforms, useTotalFollowers
} from './useSocialLinks';

// Statistics
export {
    useAchievementStatistics, useCareerStatistics,
    useSocialStatistics, useStatisticById, useStatisticCount, useStatistics, useStatisticsGrouped, useStatisticsWithTrends,
    useStatisticValue
} from './useStatistics';

// ============================================
// UTILITY HOOKS
// ============================================

// Pagination
export { usePageInfo, usePagination, usePaginationFlags } from './usePagination';

// Search & Filter
export { useFilter, useSearch, useSearchAndFilter } from './useSearch';

// Sort
export { useMultiSort, useSort, useSortCustom } from './useSort';

// Storage
export {
    useClearLocalStorage, useLocalStorage, useRemoveLocalStorageItem, useSessionStorage
} from './useStorage';

