export interface Meeting {
    id: string;
    title: string;
    date: Date;
    startTime: string;
    endTime: string;
    attendees: string[];
    notes: string;
    tags: string[];
}

export type MeetingCreate = Omit<Meeting, 'id'>;
