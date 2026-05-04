import React from 'react';
import { MainLayout, Container, Section, Grid } from '@/components/layout';
import { SectionHeader } from '@/components/common';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui';

/**
 * Portfolio Page
 * Main portfolio showcase page displaying all portfolio sections
 */
export const Portfolio: React.FC = () => {
  return (
    <MainLayout>
      {/* Hero Section */}
      <Section variant="secondary" padding="lg" id="hero">
        <Container size="lg">
          <div className="text-center space-y-6">
            <h1 className="text-5xl md:text-6xl font-bold tracking-tight">
              Welcome to My Portfolio
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Showcasing my work, experience, and expertise
            </p>
          </div>
        </Container>
      </Section>

      {/* About Section */}
      <Section padding="lg" id="about">
        <Container>
          <SectionHeader
            subtitle="Get to know me"
            title="About"
            description="Learn more about my background and expertise"
          />
          <div className="prose dark:prose-invert max-w-4xl">
            <Card>
              <CardHeader>
                <CardTitle>My Journey</CardTitle>
                <CardDescription>A brief overview of my professional background</CardDescription>
              </CardHeader>
              <CardContent>
                <p>Content will be populated from your data here...</p>
              </CardContent>
            </Card>
          </div>
        </Container>
      </Section>

      {/* Projects Section */}
      <Section variant="secondary" padding="lg" id="projects">
        <Container>
          <SectionHeader
            subtitle="My Work"
            title="Featured Projects"
            description="Here are some of my recent projects and achievements"
          />
          <Grid cols={3} gap="lg">
            {[1, 2, 3].map((item) => (
              <Card key={item} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <CardTitle>Project {item}</CardTitle>
                  <CardDescription>Project description here</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Project details and technologies will be displayed here.
                  </p>
                </CardContent>
              </Card>
            ))}
          </Grid>
        </Container>
      </Section>

      {/* Skills Section */}
      <Section padding="lg" id="skills">
        <Container>
          <SectionHeader
            subtitle="Technical Expertise"
            title="Skills"
            description="Technologies and tools I work with"
          />
          <Grid cols={2} gap="default">
            {['Frontend', 'Backend', 'Data Science', 'Tools'].map((skill) => (
              <Card key={skill}>
                <CardHeader>
                  <CardTitle className="text-lg">{skill}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Skill details will be populated here
                  </p>
                </CardContent>
              </Card>
            ))}
          </Grid>
        </Container>
      </Section>

      {/* Contact Section */}
      <Section variant="secondary" padding="lg" id="contact">
        <Container size="sm">
          <SectionHeader
            subtitle="Get in Touch"
            title="Contact"
            description="Reach out to me for opportunities and collaborations"
            className="text-center"
          />
          <Card className="mt-8">
            <CardHeader>
              <CardTitle>Let's Connect</CardTitle>
              <CardDescription>I'm always open to discussing new projects</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Contact information will be displayed here
              </p>
            </CardContent>
          </Card>
        </Container>
      </Section>
    </MainLayout>
  );
};

export default Portfolio;
