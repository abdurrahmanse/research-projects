/**
 * Data Module Index
 * Central export file for all data modules
 * This file allows easy importing of all portfolio data from a single location
 * 
 * Usage Examples:
 * import { personal, projects, skills } from '@/data';
 * import * as portfolioData from '@/data';
 * 
 * Direct module imports:
 * import { projects, getFeaturedProjects } from '@/data/projects';
 * import { blogPosts, getBlogPostsByCategory } from '@/data/blog';
 */

// Type Definitions (All types from types.ts)
export type {
    Achievement, AchievementRecord, BlogPost, CaseStudy,
    CaseStudyMetric, Certification, Education, FAQ, PersonalInfo, Project, ProjectImpact,
    ProjectLinks, Publication, Service, Skill,
    SkillCategory,
    SoftSkill, Testimonial, WorkAchievement,
    WorkExperience
} from '../types/types';

// ============================================
// PERSONAL INFORMATION
// ============================================
export { default as personal, personalInfo } from './personal';
export type { default as PersonalData } from './personal';

// ============================================
// EXPERIENCE & EDUCATION
// ============================================
export { education, default as educationData, getAllCourseworks, getCompletedEducation, getEducationById, getHighestDegree, getOngoingEducation } from './education';
export { calculateTotalExperience, default as experience, getCurrentWork, getWorkExperienceById, workExperience } from './experience';

// ============================================
// SKILLS
// ============================================
export { getAllTechnicalSkills, getExpertSkills, getSkillsByCategory, getSkillsByProficiency, getTotalEndorsements, default as skills, softSkills, technicalSkills } from './skills';

// ============================================
// PROJECTS
// ============================================
export { getFeaturedProjects, getProjectById, getProjectsByCategory as getProjectsByCategory, getProjectsByTechnology, projects, default as projectsData } from './projects';

// ============================================
// PUBLICATIONS
// ============================================
export { getAllKeywords, getMostCitedPublication, getMostDownloadedPublication, getPublicationById, getPublicationsByAuthor, getPublicationsByResearchArea, getResearchAreas, getTotalCitations, getTotalDownloads, publications, default as publicationsData } from './publications';

// ============================================
// CASE STUDIES
// ============================================
export { caseStudies, default as caseStudiesData, getCaseStudiesByCompany, getCaseStudiesByIndustry, getCaseStudyById, getCaseStudyBySlug, getCompanies as getCaseStudyCompanies, getIndustries as getCaseStudyIndustries } from './case-studies';

// ============================================
// BLOG
// ============================================
export { default as blog, blogPosts, getBlogPostById, getBlogPostBySlug, getBlogPostsByCategory as getBlogPostsByCategory, getBlogPostsByTag, getBlogPostsSortedByDate, getBlogPostsSortedByViews, getFeaturedBlogPosts, getMostViewedBlogPost, getTotalBlogViews, searchBlogPosts } from './blog';

// ============================================
// CERTIFICATIONS
// ============================================
export { certifications, default as certificationsData, getActiveCertifications, getAllCertificationSkills, getCertificationById, getCertificationByName, getIssuers as getCertificationIssuers, getCertificationsByIssuer, getCertificationsBySkill, getCertificationsExpiringSoon, getExpiredCertifications } from './certifications';

// ============================================
// ACHIEVEMENTS
// ============================================
export { achievements, default as achievementsData, getAchievementById, getCategories as getAchievementCategories, getAchievementCountByYear, getIssuers as getAchievementIssuers, getAchievementsByCategory as getAchievementsByCategory, getAchievementsByIssuer, getAchievementsSortedByDate, getFeaturedAchievements } from './achievements';

// ============================================
// TESTIMONIALS
// ============================================
export { getAverageRating, getRelationships, getTestimonialById, getCompanies as getTestimonialCompanies, getTestimonialCountByRating, getTestimonialsByCompany, getTestimonialsByRating, getTestimonialsByRelationship, getVerifiedTestimonials, testimonials, default as testimonialsData } from './testimonials';

// ============================================
// SERVICES
// ============================================
export { getFeaturedServices, getServiceById, getServicesByCategory as getServicesByCategory, getServicesByTechnology, services, default as servicesData } from './services';

// ============================================
// FAQs
// ============================================
export { faqs, default as faqsData, getFAQByCategory as getFAQByCategory, getFAQById, getCategories as getFAQCategories, getFAQsSortedByPriority, searchFAQs } from './faqs';

// ============================================
// SOCIAL LINKS
// ============================================
export { getAllSocialLinks, getPlatforms, getSocialLinkById, getSocialLinkByPlatform, getSocialLinksSortedByFollowers, getSocialLinksWithFollowers, getTotalFollowers, default as social, socialLinks, type SocialLink } from './social';

// ============================================
// STATISTICS
// ============================================
export { getAchievementStatistics, getAllStatistics, getCareerStatistics, getSocialStatistics, getStatisticById, getStatisticsWithTrends, statistics, default as statisticsData, type Statistic } from './statistics';

