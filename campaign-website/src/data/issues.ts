import { Brain, Briefcase, Building2, Leaf, Home, ShieldCheck } from "lucide-react";

export const issueCategories = [
  "Alle",
  "Utdanning + AI",
  "Første jobb",
  "Digitalisering",
  "Klima + tech",
  "Bolig + levekostnader",
  "Ansvarlig AI",
] as const;

export type IssueCategory = (typeof issueCategories)[number];

export type Issue = {
  id: string;
  title: string;
  summary: string;
  category: IssueCategory;
  tags: string[];
  impact: string;
  measures: string[];
  icon: typeof Brain;
};

export const issues: Issue[] = [
  {
    id: "utdanning-ai",
    title: "Utdanning som faktisk følger AI-skiftet",
    summary:
      "AI og digitale ferdigheter inn i alle studieretninger, med klare vurderingsformer og praktisk trening.",
    category: "Utdanning + AI",
    tags: ["Campus", "AI", "Praksis"],
    impact:
      "Studenter møter arbeidslivet med dokumenterbar kompetanse og ansvarlig AI-bruk.",
    measures: [
      "Nasjonale retningslinjer for AI i undervisning og vurdering",
      "AI- og dataforståelse i alle studieprogrammer",
      "Casebasert undervisning i samarbeid med arbeidslivet",
    ],
    icon: Brain,
  },
  {
    id: "forste-jobb",
    title: "En tryggere vei inn i første jobb",
    summary:
      "Betalte trainee-løp, mentorordninger og insentiver for ansettelse av nyutdannede.",
    category: "Første jobb",
    tags: ["Trainee", "Arbeidsliv"],
    impact: "Kortere vei til første jobb og færre som faller utenfor.",
    measures: [
      "Første jobb-løp med veiledning og lønnsstøtte",
      "Skatteinsentiver for nyutdannede i faste roller",
      "Tett kobling mellom utdanning og reelle oppdrag",
    ],
    icon: Briefcase,
  },
  {
    id: "digitalisering",
    title: "Offentlig digitalisering med brukerfokus",
    summary:
      "Sømløse tjenester, ansvarlig AI og offentlig–privat samarbeid som gir bedre opplevelser.",
    category: "Digitalisering",
    tags: ["Offentlig", "UX"],
    impact: "Mindre byråkrati og tryggere digitale tjenester.",
    measures: [
      "Felles standarder for dataflyt og sikkerhet",
      "Etiske retningslinjer for AI i offentlig sektor",
      "Produktteam med brukertesting og målt effekt",
    ],
    icon: Building2,
  },
  {
    id: "klima-tech",
    title: "Klima + tech som virker i hverdagen",
    summary:
      "Teknologi som gir målbare utslippskutt i transport, bygg og industri.",
    category: "Klima + tech",
    tags: ["Mobilitet", "Energi"],
    impact: "Lavere utslipp og smartere drift i offentlig og privat sektor.",
    measures: [
      "Grønne krav i offentlige IT-anskaffelser",
      "Insentiver for energieffektiv programvare og sky",
      "Støtte til tech-prosjekter som kutter utslipp",
    ],
    icon: Leaf,
  },
  {
    id: "bolig",
    title: "Bolig som er mulig å leve i",
    summary:
      "Flere student- og startboliger, bedre leieforhold og sterkere kollektivtilbud.",
    category: "Bolig + levekostnader",
    tags: ["Bolig", "Levekost"],
    impact: "Forutsigbare levekostnader og kortere vei til campus og jobb.",
    measures: [
      "Flere studentboliger i pressområder",
      "Tiltak for rimelig leie nær campus og arbeidsklynger",
      "Bedre kollektivtilbud rundt studie- og jobbknutepunkt",
    ],
    icon: Home,
  },
  {
    id: "ansvarlig-ai",
    title: "Ansvarlig AI og personvern",
    summary:
      "Sikkerhet, innsyn og kvalitet som tåler offentlighet.",
    category: "Ansvarlig AI",
    tags: ["Personvern", "Rettigheter"],
    impact: "Trygg teknologi som bygger tillit, ikke overvåking.",
    measures: [
      "Standarder for ansvarlig AI i offentlig og privat sektor",
      "Rett til forklaring i automatiserte vedtak",
      "Sikkerhet og kvalitet som krav i alle prosjekter",
    ],
    icon: ShieldCheck,
  },
];
