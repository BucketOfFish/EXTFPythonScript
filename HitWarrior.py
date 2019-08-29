import numpy as np


def overlapRemoval(tracks):
    '''Given a set of tracks, we cluster them into matching tracks, and return the set of best tracks from each
    cluster in the form [[[best track coordinates], [fit params], chi2]...].'''

    def matching_track_clusters(tracks):
        '''Given an array of tracks, return a list of matching (sharing 6 or more hits) track indices.
        e.g. Given 5 tracks, where tracks 0 and 1 match, and tracks 3 and 4 match, return [[0,1], [2], [3,4]].
        Note that if tracks 0 and 1 match, and tracks 1 and 2 match, we consider tracks 0 and 2 to match.'''

        def n_matching_hits(track_i, track_j):
            '''Number of matching hits (IBL+SCT) between two tracks.'''
            matches = [i == j for i, j in zip(track_i[0], track_j[0])]
            n_IBL_matches = (matches[0] & matches[1]) + (matches[2] & matches[3]) + (matches[4] & matches[5]) + (matches[6] & matches[7])
            n_SCT_matches = sum(matches[8:16])
            return n_IBL_matches + n_SCT_matches

        track_clusters = []
        for i in range(len(tracks)):
            current_cluster = []
            for j in range(i, len(tracks)):
                if n_matching_hits(tracks[i], tracks[j]) > 6:
                    current_cluster.append(j)
            is_new_cluster = True
            for n, cluster in enumerate(track_clusters):
                combined_cluster = set(cluster+current_cluster)
                if len(combined_cluster) < len(cluster) + len(current_cluster):
                    track_clusters[n] = list(combined_cluster)
                    is_new_cluster = False
                    break
            if is_new_cluster:
                track_clusters.append(current_cluster)

        track_clusters = [np.array(i) for i in track_clusters]
        return track_clusters

    def best_track(track_cluster, tracks):
        '''For each track cluster, return the index of the track with the best fit parameters (lowest chi2 out of
        tracks with most layer map hits).'''
        nonzero_coords_v = [[i != -1 for i in tracks[cluster, 0]] for cluster in track_cluster]
        chisq_v = [tracks[cluster, 2] for cluster in track_cluster]
        indices_with_max_nonzero_coords = np.where([i == max(nonzero_coords_v) for i in nonzero_coords_v])[0]
        best_index = chisq_v.index(min(np.array(chisq_v)[indices_with_max_nonzero_coords]))
        return tracks[track_cluster[best_index]]

    track_clusters = matching_track_clusters(tracks)
    uniqueTracks = [best_track(cluster, np.array(tracks)) for cluster in track_clusters]
    return uniqueTracks
