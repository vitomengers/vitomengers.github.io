// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about-me",
    title: "About Me",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-news",
          title: "News",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/news/";
          },
        },{id: "nav-publications",
          title: "Publications",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-teaching",
          title: "Teaching",
          description: "Teaching and advising experience.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/teaching/";
          },
        },{id: "nav-talks-amp-outreach",
          title: "Talks &amp; Outreach",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/talks&outreach/";
          },
        },{id: "nav-cv",
          title: "CV",
          description: "For publications, teaching experience, and outreach activities, see menu points above.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "post-google-gemini-updates-flash-1-5-gemma-2-and-project-astra",
        
          title: 'Google Gemini updates: Flash 1.5, Gemma 2 and Project Astra <svg width="1.2rem" height="1.2rem" top=".5rem" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg"><path d="M17 13.5v6H5v-12h6m3-3h6v6m0-6-9 9" class="icon_svg-stroke" stroke="#999" stroke-width="1.5" fill="none" fill-rule="evenodd" stroke-linecap="round" stroke-linejoin="round"></path></svg>',
        
        description: "We’re sharing updates across our Gemini family of models and a glimpse of Project Astra, our vision for the future of AI assistants.",
        section: "Posts",
        handler: () => {
          
            window.open("https://blog.google/technology/ai/google-gemini-update-flash-ai-assistant-io-2024/", "_blank");
          
        },
      },{id: "post-displaying-external-posts-on-your-al-folio-blog",
        
          title: 'Displaying External Posts on Your al-folio Blog <svg width="1.2rem" height="1.2rem" top=".5rem" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg"><path d="M17 13.5v6H5v-12h6m3-3h6v6m0-6-9 9" class="icon_svg-stroke" stroke="#999" stroke-width="1.5" fill="none" fill-rule="evenodd" stroke-linecap="round" stroke-linejoin="round"></path></svg>',
        
        description: "",
        section: "Posts",
        handler: () => {
          
            window.open("https://medium.com/@al-folio/displaying-external-posts-on-your-al-folio-blog-b60a1d241a0a?source=rss-17feae71c3c4------2", "_blank");
          
        },
      },{id: "books-the-godfather",
          title: 'The Godfather',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/the_godfather/";
            },},{id: "news-official-start-of-this-webpage",
          title: 'Official start of this webpage 🎉',
          description: "",
          section: "News",},{id: "news-our-paper-a-robotics-inspired-scanpath-model-reveals-the-importance-of-uncertainty-and-semantic-object-cues-for-gaze-guidance-in-dynamic-scenes-was-accepted-at-the-journal-of-vision",
          title: 'Our paper A robotics-inspired scanpath model reveals the importance of uncertainty and semantic...',
          description: "",
          section: "News",},{id: "news-lab-demos-for-giovanni-beltrame-and-stephen-fiore",
          title: 'Lab demos for Giovanni Beltrame and Stephen Fiore.',
          description: "",
          section: "News",},{id: "news-two-papers-accepted-at-icra25",
          title: 'Two papers accepted at ICRA25!',
          description: "",
          section: "News",},{id: "news-lab-demo-for-tucker-hermans",
          title: 'Lab demo for Tucker Hermans.',
          description: "",
          section: "News",},{id: "news-two-poster-presentations-today-at-the-german-robotics-conference",
          title: 'Two poster presentations today at the German Robotics Conference.',
          description: "",
          section: "News",},{id: "news-lab-demo-for-another-vito-vito-trianni",
          title: 'Lab demo for another Vito – Vito Trianni.',
          description: "",
          section: "News",},{id: "news-our-paper-no-plan-but-everything-under-control-robustly-solving-sequential-tasks-with-dynamically-composed-gradient-descent-is-nominated-for-icra25-best-paper",
          title: 'Our paper No Plan but Everything Under Control: Robustly Solving Sequential Tasks with...',
          description: "",
          section: "News",},{id: "news-lab-demo-for-kevin-o-regan",
          title: 'Lab demo for Kevin O’Regan.',
          description: "",
          section: "News",},{id: "news-two-conference-paper-presentations-and-two-workshop-presentations-over-the-next-days-at-icra",
          title: 'Two conference paper presentations and two workshop presentations over the next days at...',
          description: "",
          section: "News",},{id: "news-icra-best-paper-in-planning-and-control-for-our-paper-no-plan-but-everything-under-control-robustly-solving-sequential-tasks-with-dynamically-composed-gradient-descent",
          title: 'ICRA Best Paper in Planning and Control for our paper No Plan but...',
          description: "",
          section: "News",},{id: "news-lab-demo-for-tony-prescott",
          title: 'Lab demo for Tony Prescott.',
          description: "",
          section: "News",},{id: "news-lab-demo-for-fumiya-iida",
          title: 'Lab demo for Fumiya Iida.',
          description: "",
          section: "News",},{id: "news-lab-demo-for-john-tsotsos",
          title: 'Lab demo for John Tsotsos.',
          description: "",
          section: "News",},{id: "news-lab-demo-for-dario-floreano",
          title: 'Lab demo for Dario Floreano.',
          description: "",
          section: "News",},{id: "news-lab-demo-for-will-warren",
          title: 'Lab demo for Will Warren.',
          description: "",
          section: "News",},{id: "news-lab-demo-for-jacob-yates",
          title: 'Lab demo for Jacob Yates.',
          description: "",
          section: "News",},{id: "news-i-was-interviewed-for-the-robotics-and-automation-magazine-find-the-interview-here",
          title: 'I was interviewed for the Robotics and Automation Magazine. Find the interview here!...',
          description: "",
          section: "News",},{id: "news-lab-demo-and-participation-at-the-rig-technical-committee-workshop-manipulate-anything-anywhere-anytime",
          title: 'Lab demo and participation at the RIG Technical Committee Workshop “Manipulate Anything, Anywhere,...',
          description: "",
          section: "News",},{id: "news-i-participated-in-the-berlin-science-week-science-slam-see-my-slam-here",
          title: 'I participated in the Berlin Science Week Science Slam! See my slam here....',
          description: "",
          section: "News",},{id: "news-i-was-interviewed-for-the-podcast-series-of-the-german-research-foundation-on-excellent-research-find-the-exzellent-erklärt-episode-here-in-german",
          title: 'I was interviewed for the podcast series of the German Research Foundation on...',
          description: "",
          section: "News",},{id: "news-one-paper-accepted-at-icra26",
          title: 'One paper accepted at ICRA26!',
          description: "",
          section: "News",},{id: "news-lab-demo-for-thomas-dohmke",
          title: 'Lab demo for Thomas Dohmke.',
          description: "",
          section: "News",},{id: "news-a-poster-presentation-today-at-the-german-robotics-conference",
          title: 'A poster presentation today at the German Robotics Conference.',
          description: "",
          section: "News",},{id: "outreach-participation-in-i-m-a-scientist-get-me-out-of-here",
          title: 'Participation in “I’m a Scientist – Get Me Out of Here!”',
          description: "Participation in a nationwide dialogue initiative connecting school students directly with researchers",
          section: "Outreach",handler: () => {
              window.location.href = "/outreach/22_im_a_scientist/";
            },},{id: "outreach-girl-39-s-day-at-science-of-intelligence",
          title: 'Girl&amp;#39;s Day at Science of Intelligence',
          description: "Full-day event to inspire German school girls to pursue a career in science",
          section: "Outreach",handler: () => {
              window.location.href = "/outreach/23_girlsday/";
            },},{id: "outreach-interactive-presentation-and-demo-at-the-alexander-von-humboldt-foundation-s-annual-alumni-event",
          title: 'Interactive Presentation and Demo at the Alexander von Humboldt Foundation’s Annual Alumni Event...',
          description: "Interdisciplinary Exchanges &amp; Public Outreach",
          section: "Outreach",handler: () => {
              window.location.href = "/outreach/24_avh/";
            },},{id: "outreach-podcast-interview-about-my-research-in-german",
          title: 'Podcast Interview About My Research (in German)',
          description: "Podcast of the DFG (German Research Foundation) &quot;Exzellent Erklärt&quot;",
          section: "Outreach",handler: () => {
              window.location.href = "/outreach/25_podcast/";
            },},{id: "outreach-science-slam-at-the-berlin-science-week",
          title: 'Science Slam at the Berlin Science Week',
          description: "Title of my Slam -- &quot;Why my robot is still stupid&quot;",
          section: "Outreach",handler: () => {
              window.location.href = "/outreach/25_science_slam/";
            },},{id: "projects-project-10",
          title: 'project 10',
          description: "A project with an introduction section",
          section: "Projects",handler: () => {
              window.location.href = "/projects/10_project/";
            },},{id: "talks-talk-scioi-s-scientific-networking-days-differentiable-interconnected-recursive-estimation",
          title: 'Talk @ SCIoI’s Scientific Networking Days Differentiable Interconnected Recursive Estimation',
          description: "",
          section: "Talks",},{id: "talks-poster-icra23-combining-motion-and-appearance-for-robust-probabilistic-object-segmentation-in-real-time-together-with-manuel-baum",
          title: 'Poster @ ICRA23 Combining Motion and Appearance for Robust Probabilistic Object Segmentation in...',
          description: "",
          section: "Talks",},{id: "talks-invited-talk-iridia-seminar-université-libre-de-bruxelles-from-segmentation-to-collaboration-exploring-the-role-of-robust-estimation-of-object-segmentation-in-achieving-robust-collective-estimation",
          title: 'Invited Talk @ IRIDIA Seminar (Université Libre de Bruxelles) From Segmentation to Collaboration:...',
          description: "",
          section: "Talks",},{id: "talks-talk-scioi-s-scientific-networking-days-interdisciplinary-applications-of-interconnected-recursive-estimators",
          title: 'Talk @ SCIoI’s Scientific Networking Days   Interdisciplinary Applications of Interconnected Recursive Estimators',
          description: "",
          section: "Talks",},{id: "talks-talk-scioi-s-thursday-morning-talks-principles-at-play-what-is-intelligence-together-with-aravind-battaje",
          title: 'Talk @ SCIoI’s Thursday Morning Talks Principles at Play: What is Intelligence? –...',
          description: "",
          section: "Talks",},{id: "talks-talk-netsci24-centrality-certainty-correlation-in-heterogeneous-opinion-dynamics-together-with-mohsen-raoufi",
          title: 'Talk @ NetSci24 Centrality-Certainty Correlation in Heterogeneous Opinion Dynamics – Together with Mohsen...',
          description: "",
          section: "Talks",},{id: "talks-talk-amp-amp-poster-scioi-s-scientific-networking-days-gradient-descent-through-interconnected-recursive-estimators",
          title: 'Talk &amp;amp;amp; Poster @ SCIoI’s Scientific Networking Days Gradient Descent through Interconnected Recursive...',
          description: "",
          section: "Talks",},{id: "talks-poster-grc25-aicon-a-representation-for-adaptive-behavior",
          title: 'Poster @ GRC25   AICON: A Representation for Adaptive Behavior',
          description: "",
          section: "Talks",},{id: "talks-poster-grc25-a-handy-solution-to-kinematic-structure-estimation-together-with-adrian-pfisterer",
          title: 'Poster @ GRC25 A Handy Solution to Kinematic Structure Estimation – Together with...',
          description: "",
          section: "Talks",},{id: "talks-poster-icra25-workshop-learning-meets-model-based-methods-for-contact-rich-manipulation-stop-merging-start-separating-why-merging-learning-and-modeling-won-t-solve-manipulation-but-separating-the-general-from-the-specific-will",
          title: 'Poster @ ICRA25 Workshop “Learning Meets Model-Based Methods for Contact-Rich Manipulation” Stop Merging,...',
          description: "",
          section: "Talks",},{id: "talks-talk-amp-amp-poster-icra25-no-plan-but-everything-under-control-robustly-solving-sequential-tasks-with-dynamically-composed-gradient-descent",
          title: 'Talk &amp;amp;amp; Poster @ ICRA25 No Plan but Everything Under Control: Robustly Solving...',
          description: "",
          section: "Talks",},{id: "talks-poster-icra25-workshop-beyond-the-lab-robust-planning-and-control-in-real-world-scenarios-no-plan-but-everything-under-control",
          title: 'Poster @ ICRA25 Workshop “Beyond the Lab: Robust Planning and Control in Real...',
          description: "",
          section: "Talks",},{id: "teachings-responsible-for-exercises-basics-of-robot-control",
          title: 'Responsible for Exercises — Basics of Robot Control',
          description: "Exercise instructor and assessor for course &quot;Robotics&quot;.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/21_robotics/";
            },},{id: "teachings-responsible-for-exercises-recursive-estimation",
          title: 'Responsible for Exercises — Recursive Estimation',
          description: "Exercise instructor and assessor for course &quot;Robotics&quot;.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/22_robotics/";
            },},{id: "teachings-advisor-course-quot-robotics-project-quot",
          title: 'Advisor — Course &amp;quot;Robotics Project&amp;quot;',
          description: "Supervised student projects, guided presentations and report writing, provided technical mentorship.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/22_robotics_project/";
            },},{id: "teachings-advisor-course-quot-robotics-seminar-quot",
          title: 'Advisor — Course &amp;quot;Robotics Seminar&amp;quot;',
          description: "Supervised student presentations and writing, facilitated seminar discussions.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/22_robotics_seminar/";
            },},{id: "teachings-responsible-for-exercises-visual-servoing",
          title: 'Responsible for Exercises — Visual Servoing',
          description: "Exercise instructor and assessor for course &quot;Robotics&quot;.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/23_robotics/";
            },},{id: "teachings-advisor-master-thesis-quot-tracking-hand-motion-to-infer-object-motion-constraints-quot",
          title: 'Advisor — Master Thesis &amp;quot;Tracking Hand Motion to Infer Object Motion Constraints&amp;quot;',
          description: "Co-Advised with Xing Li; Supervised and Examined by Oliver Brock &amp; Guillermo Gallego; **Winner of the Rolf-Niedermeier-Award**",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/24_ms_adrian/";
            },},{id: "teachings-advisor-master-thesis-quot-estimating-robust-affordances-from-vision-by-combining-multiple-models-quot",
          title: 'Advisor — Master Thesis &amp;quot;Estimating Robust Affordances from Vision by Combining Multiple Models&amp;quot;...',
          description: "Supervised and Examined by Oliver Brock &amp; Guillermo Gallego",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/24_ms_patrick/";
            },},{id: "teachings-responsible-for-exercises-amp-lecture-advanced-robot-control",
          title: 'Responsible for Exercises &amp;amp; Lecture — Advanced Robot Control',
          description: "Lecture delivery and exercise supervision in course &quot;Robotics&quot;.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/24_robotics/";
            },},{id: "teachings-advisor-course-quot-robotics-seminar-quot",
          title: 'Advisor — Course &amp;quot;Robotics Seminar&amp;quot;',
          description: "Supervised student presentations and writing, facilitated seminar discussions.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/24_robotics_seminar/";
            },},{id: "teachings-advisor-master-thesis-quot-comparing-the-mechanisms-of-plan-generation-in-humans-and-machines-via-failure-modes-quot",
          title: 'Advisor — Master Thesis &amp;quot;Comparing the Mechanisms of Plan Generation in Humans and...',
          description: "Supervised and Examined by Oliver Brock &amp; Eva Wiese",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/25_ms_antonia/";
            },},{id: "teachings-advisor-master-thesis-quot-dynamically-leveraging-sensorimotor-regularities-by-integrating-perception-and-behavior-generation-quot",
          title: 'Advisor — Master Thesis &amp;quot;Dynamically Leveraging Sensorimotor Regularities by Integrating Perception and Behavior...',
          description: "Co-Advised with Aravind Battaje &amp; Alexander Koenig; Supervised and Examined by Oliver Brock &amp; Marc Toussaint",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/25_ms_malte/";
            },},{id: "teachings-responsible-for-exercises-amp-lecture-motion-planning",
          title: 'Responsible for Exercises &amp;amp; Lecture — Motion Planning',
          description: "Lecture delivery and exercise supervision in course &quot;Robotics&quot;.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/25_robotics/";
            },},{id: "teachings-advisor-course-quot-robotics-project-quot",
          title: 'Advisor — Course &amp;quot;Robotics Project&amp;quot;',
          description: "Supervised student projects, guided presentations and report writing, provided technical mentorship.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/25_robotics_project/";
            },},{id: "teachings-advisor-master-thesis-quot-active-interconnections-as-a-mechanistic-model-for-collective-behavior-quot",
          title: 'Advisor — Master Thesis &amp;quot;Active Interconnections as a Mechanistic Model for Collective Behavior&amp;quot;...',
          description: "Supervised and Examined by Oliver Brock &amp; Pawel Romanczuk",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/26_ms_duc/";
            },},{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%76.%6D%65%6E%67%65%72%73@%74%75-%62%65%72%6C%69%6E.%64%65", "_blank");
        },
      },{
        id: 'social-scholar',
        title: 'Google Scholar',
        section: 'Socials',
        handler: () => {
          window.open("https://scholar.google.com/citations?user=4Yp4lRwAAAAJ", "_blank");
        },
      },{
        id: 'social-linkedin',
        title: 'LinkedIn',
        section: 'Socials',
        handler: () => {
          window.open("https://www.linkedin.com/in/vito-mengers", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
